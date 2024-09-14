import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm


def get_fixtures(teams, competitions, root_path):
    all_fixtures = []
    print('teams')
    print('get fixtures')

    if 'laliga' in competitions:
        laliga_file = open(f'{root_path}laliga_fixtures.json')
        data = json.load(laliga_file)
        all_fixtures.extend(data)
    
    if 'epl' in competitions:
        epl_file = open(f'{root_path}epl_fixtures.json')
        data = json.load(epl_file)
        all_fixtures.extend(data)
    
    if 'ucl' in competitions:
        epl_file = open(f'{root_path}ucl_fixtures.json')
        data = json.load(epl_file)
        all_fixtures.extend(data)

    #print(f'all fixtures {len(all_fixtures)}')
    
    wanted_fixtures = [d for d in all_fixtures if d['home'] in teams or d['away'] in teams]
    
    #print('wanted fixtures')
    #print(wanted_fixtures)

    return wanted_fixtures

def create_fixtures_ics(fixtures, temp_dir):
    filename = f'{temp_dir}/fixture.ics'
    cal = Calendar()
    current_month = datetime.now().month
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')

    for i in fixtures:
        #print(i['time'])
        if '/' in i['time']:
            fixture_month = int(i['time'].split('/')[1].split(' ')[0])
        else:
            break
        year = 2024 if fixture_month >= current_month else 2025
        start_date = datetime.strptime(f"{i['time']} {year}", "%d/%m %H:%M %Y")
        start_date = start_date - timedelta(hours=1)
        summary = f"Match day: {i['match_day']} {i['home']} vs {i['away']}"
        event = Event()
        event.add('summary', summary)
        event.add('dtstart', start_date)

        alarm = Alarm()
        alarm.add('trigger', timedelta(minutes=-30))  # Reminder 30 minutes before the event
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f'Reminder for {summary}')
        event.add_component(alarm)
        cal.add_component(event)
        #print(f'created a calendar event for {i['match_day']}')
    
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    return filename

# def create_ics_file(start_date_str, end_date_str, summary, description, filename):
#     # Set the year as 2024
#     year = 2024

#     # Convert the input date strings to datetime objects with the year 2024
#     start_date = datetime.strptime(f'{start_date_str} {year}', "%d/%m %H:%M %Y")
#     #end_date = datetime.strptime(f'{end_date_str} {year}', "%d/%m %H:%M %Y")

#     # Create a calendar and an event
#     cal = Calendar()
#     event = Event()

#     # Set the event's details
#     event.add('summary', summary)
#     event.add('description', description)
#     event.add('dtstart', start_date)
#     #event.add('dtend', end_date)

#     # Create a reminder (Alarm)
#     alarm = Alarm()
#     alarm.add('trigger', timedelta(minutes=-15))  # Reminder 15 minutes before the event
#     alarm.add('action', 'DISPLAY')
#     alarm.add('description', f'Reminder for {summary}')

#     # Add the alarm to the event
#     event.add_component(alarm)

#     # Add the event to the calendar
#     cal.add_component(event)

#     # Write to .ics file
#     with open(f'{filename}.ics', 'wb') as f:
#         f.write(cal.to_ical())
    
#     return f'{filename}.ics'