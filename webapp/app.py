from flask import Flask, render_template, request, send_file
from utils import get_fixtures, create_fixtures_ics
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def uploadForm():
    if request.method == 'POST':
        temp_dir = tempfile.TemporaryDirectory()
        selected_teams = request.form.getlist('team')
        selected_competitions = request.form.getlist('competition')
        root_path = os.path.join(app.root_path, 'static/fixtures/')
        club_fixtures = get_fixtures(selected_teams, selected_competitions, root_path)
        file_download = create_fixtures_ics(club_fixtures, temp_dir.name)
        print(selected_teams)
        print(selected_competitions)
        print(len(club_fixtures))
        #file_download = create_ics_file('17/08 16:00', '17/08 17:00', 'Meeting with Team', 'Discuss project progress', 'meeting_event')
        return send_file(file_download, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)