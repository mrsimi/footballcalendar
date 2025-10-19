import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import requests
from bs4 import BeautifulSoup

def download_fixtures_to_json(url, competition):
    print(f"Crawling fixtures for {competition}...")
    response = requests.get(url)
    fixtures = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        matchday_divs = soup.find_all("div", class_="jornada calendarioInternacional")

        index = 1
        for matchday_div in matchday_divs:
            matches = matchday_div.find_all("tr")
            for match in matches:
                home = match.find("td", class_="local")
                time = match.find("td", class_="resultado")
                away = match.find("td", class_="visitante")

                if home and time and away and '-' not in time.text.strip():
                    fixtures.append({
                        'home': home.text.strip(),
                        'time': time.text.strip(),
                        'away': away.text.strip(),
                        'match_day': index,
                        'competition': competition
                    })
            index += 1

    print(f"✅ {competition}: {len(fixtures)} fixtures downloaded.")
    return fixtures


def get_fixtures(teams, competitions, cache):
    urls = {
        'epl': 'https://www.marca.com/en/football/premier-league/schedule.html?intcmp=MENUPROD&s_kw=soccer-premier-league-schedule',
        'laliga': 'https://www.marca.com/en/football/spanish-football/liga/schedule.html?intcmp=MENUPROD&s_kw=soccer-laliga-schedule',
        'ucl': 'https://www.marca.com/en/football/champions-league/schedule.html?intcmp=MENUPROD&s_kw=soccer-champions-league-schedule'
    }

    all_fixtures = []
    print("Fetching fixtures...")

    for comp in competitions:
        cache_key = f"fixtures:{comp}"

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"Cache hit — using cached {comp} fixtures.")
            fixtures = cached_data
        else:
            print(f"Cache miss — crawling {comp} fixtures.")
            fixtures = download_fixtures_to_json(urls[comp], comp)
            cache.set(cache_key, fixtures)

        all_fixtures.extend(fixtures)

    # Filter fixtures for selected teams
    wanted_fixtures = [
        f for f in all_fixtures
        if f['home'] in teams or f['away'] in teams
    ]

    print(f"Total fixtures after filtering: {len(wanted_fixtures)}")
    return wanted_fixtures
def create_fixtures_ics(fixtures, temp_dir):
    import os
    from datetime import datetime, timedelta
    from icalendar import Calendar, Event, Alarm, Timezone, TimezoneStandard, TimezoneDaylight
    import pytz

    tz = pytz.timezone("Europe/Madrid")
    filename = os.path.join(temp_dir, 'fixture.ics')

    # Always start with a fresh file
    if os.path.exists(filename):
        os.remove(filename)

    cal = Calendar()
    cal.add('prodid', '-//Football Calendar//example.com//')
    cal.add('version', '2.0')

    # Add explicit timezone block (so calendars interpret correctly)
    tz_component = Timezone()
    tz_component.add('tzid', 'Europe/Madrid')

    # Standard time
    standard = TimezoneStandard()
    standard.add('tzname', 'CET')
    standard.add('dtstart', datetime(1970, 10, 25, 3, 0, 0))
    standard.add('tzoffsetfrom', timedelta(hours=2))
    standard.add('tzoffsetto', timedelta(hours=1))
    tz_component.add_component(standard)

    # Daylight saving time
    daylight = TimezoneDaylight()
    daylight.add('tzname', 'CEST')
    daylight.add('dtstart', datetime(1970, 3, 29, 2, 0, 0))
    daylight.add('tzoffsetfrom', timedelta(hours=1))
    daylight.add('tzoffsetto', timedelta(hours=2))
    tz_component.add_component(daylight)

    cal.add_component(tz_component)

    now = datetime.now(tz)
    current_year = now.year
    current_month = now.month

    for fixture in fixtures:
        time_str = fixture.get('time', '').strip()
        if '/' not in time_str:
            continue

        try:
            day = int(time_str.split('/')[0])
            month = int(time_str.split('/')[1].split(' ')[0])
            hour_minute = time_str.split(' ')[1]
            hour, minute = map(int, hour_minute.split(':'))
        except (IndexError, ValueError):
            continue

        # If fixture month < current month → next year
        year = current_year if month >= current_month else current_year + 1

        # Localize using Europe/Madrid
        start_date_local = tz.localize(datetime(year, month, day, hour, minute))

        summary = f"{fixture['competition'].upper()} Matchday {fixture['match_day']}: {fixture['home']} vs {fixture['away']}"

        event = Event()
        event.add('summary', summary)
        event.add('dtstart', start_date_local)
        event.add('dtend', start_date_local + timedelta(hours=2))  # assume 2h match
        event.add('dtstamp', datetime.now(tz))
        event.add('location', fixture['home'])

        # Reminder 30 mins before kickoff
        alarm = Alarm()
        alarm.add('trigger', timedelta(minutes=-30))
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f"Reminder for {summary}")
        event.add_component(alarm)

        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ iCalendar file created with Europe/Madrid timezone at: {filename}")
    return filename

