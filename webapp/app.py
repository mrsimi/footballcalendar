from flask import Flask, render_template, request, Response, jsonify
from flask_caching import Cache
from utils import get_fixtures, create_fixtures_ics
import tempfile, hashlib, time, os
from urllib.parse import quote

app = Flask(__name__)

# 🧠 Cache setup (48 hours)
app.config.update(
    CACHE_TYPE="SimpleCache",
    CACHE_DEFAULT_TIMEOUT=60 * 60 * 48  # 48 hours
)
cache = Cache(app)


@app.route("/", methods=["GET"])
def index():
    """Render homepage with upload form."""
    return render_template("index.html")


@app.route('/generate', methods=['POST'])
def generate_ics():
    teams = request.form.getlist('team[]')
    competitions = request.form.getlist('competition')

    if not teams or not competitions:
        return "Missing teams or competitions", 400

    base_url = request.host_url.rstrip("/")

    # ✅ Encode each segment so spaces -> %20 etc.
    teams_query = ','.join(quote(t.strip()) for t in teams)
    competition_query = ','.join(quote(c.strip()) for c in competitions)

    ics_url = f"{base_url}/calendar/{competition_query}/{teams_query}.ics"

    return jsonify({"ics_url": ics_url})


@app.route('/calendar/<competitions>/<teams>.ics')
def calendar_feed(competitions, teams):
    teams = teams.split(',')
    competitions = competitions.split(',')

    if not teams or not competitions:
        return Response("Missing teams or competitions", status=400)

    # Unique cache key based on selected parameters
    cache_key = f"ics:{','.join(sorted(teams))}:{','.join(sorted(competitions))}"

    cached_response = cache.get(cache_key)
    if cached_response:
        # Check for client ETag
        if request.headers.get("If-None-Match") == cached_response["etag"]:
            return Response(status=304)

        # Return cached version
        return Response(
            cached_response["data"],
            mimetype="text/calendar",
            headers=cached_response["headers"]
        )

    # 🧩 Generate fresh ICS
    fixtures = get_fixtures(teams, competitions, cache)
    tmp_dir = tempfile.gettempdir()
    ics_path = create_fixtures_ics(fixtures, tmp_dir)

    with open(ics_path, "rb") as f:
        ics_data = f.read()
        etag = hashlib.md5(ics_data).hexdigest()

    headers = {
        "Content-Disposition": "inline; filename=fixtures.ics",
        "ETag": etag,
        "Cache-Control": "public, max-age=3600",  # Clients can cache 1 hour
        "Last-Modified": time.strftime(
            "%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(ics_path))
        ),
    }

    # Store in memory cache
    cache.set(cache_key, {"data": ics_data, "etag": etag, "headers": headers})

    return Response(ics_data, mimetype="text/calendar", headers=headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
