import csv
from ics import Event, Calendar
from datetime import timezone
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from ics.grammar.parse import ContentLine
from pprint import pprint

c = Calendar(creator='-//YB/classes//EN')
locations = {'Comp Sci': 'Computer room grade 7', 'Hebrew':'ה2', 'Tanach':'ה2', 'Literature':'ה2',
             'Civics':'ה2', 'Education':'ה2', 'History':'ה2', 'Physics':'ה1', 'Math':'ה7',
             'English':'Computer room Ofek', 'Gym':''}
events = []

with open('classes.csv', newline='') as file:
    for row in file:
        row = row.replace('ï»¿', '').split(',')
        for i in range(len(row)):
            row[i] = row[i].strip()

        events += [Event(row[i+2],
                         dt(2025, 9, 7+i, int(row[0][:2]), int(row[0][2:]), tzinfo=ZoneInfo('Asia/Jerusalem')),
                         dt(2025, 9, 7+i, int(row[1][:2]), int(row[1][2:]), tzinfo=ZoneInfo('Asia/Jerusalem')),
                         location=locations[row[i+2]])
                         for i in range(len(row[2:])) if row[i+2] != '']

events = sorted(events, key=lambda e: e.begin.datetime.day)
i = 0
for event in events:
    if event.name == events[i+1].name and event.end == events[i+1].begin:
        events[i+1] = Event(event.name, event.begin, events[i+1].end, location=event.location)
        events.remove(event)
for e in events:
    e.extra.append(ContentLine("DTSTAMP", value=dt.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")))
    e.extra.append(ContentLine('RRULE', value="FREQ=WEEKLY;UNTIL=20260620T165959Z"))
    c.events.add(e)

with open('classes.ics', 'w', encoding='utf-8', newline='') as file:
    file.writelines(c.serialize_iter())
