import typer
from ics import Event, Calendar
from arrow import Arrow
from datetime import date, timedelta

app = typer.Typer()

@app.command()
def add(args: list[str]):
    try:
        with open('events.ics', 'r') as file:
            c = Calendar(file)
            for item in args:
                date,name = item.split(';')
                date = [int(n) for n in date.split('/')]
                c.events.add(Event(name, Arrow(date[0], date[1], date[2])))
        with open('events.ics', 'w', encoding='utf-8', newline='') as file:
            file.writelines(c.serialize_iter())

    except FileNotFoundError:
        c = Calendar()
        date, name = args[0].split(';')
        date = [int(n) for n in date.split('/')]
        c.events.add(Event(name, Arrow(date[0], date[1], date[2])))
        with open('events.ics', 'w', newline='', encoding='utf-8') as file:
            file.writelines(c.serialize_iter())
        try:
            add(args[1:])
        except IndexError:
            pass

def str_to_date(string):
    if '-' in string:
        begin, end = string.split('-')
        begin = [int(n) for n in begin.split('/')]
        begin = date(begin[2], begin[1], begin[0])
        end = [int(n) for n in end.split('/')]
        end = date(end[2], end[1], end[0])
        current = begin
        toReturn = [begin]
        while(current!=end):
            current+=timedelta(1)
            toReturn.append(current)
        return toReturn
    else:
        time = [int(n) for n in string.split('/')]
        return [date(time[2], time[1], time[0])]
            
@app.command()
def remove(args: list[str]):
    for item in args:
        with open('events.ics', 'r') as file:
            c = Calendar(file)
        try:
            date,name = item.split(';')
            date = [int(n) for n in date.split('/')]
            c.events.remove(Event(name, Arrow(date[0], date[1], date[2])))
            with open('events.py', 'w', newline='', encoding='utf-8') as file:
                file.writelines(c.serialize_iter)
        except KeyError:
            print('Event not in calendar')

@app.command()
def blackout(args: list[str]):
    with open('classes.ics', 'r') as file:
        c = Calendar(file)
    dates = [str_to_date(i) for i in args]
    
@app.command()
def timezone(path: str):
    with open(path, 'r', newline='', encoding='utf-8') as file:
        file = file.read()
        c = Calendar(file)
    dst_start = date(2025, 10, 25)
    dst_end = date(2026, 3, 28)
    for event in c.events:
        if dst_start < event.begin.date() < dst_end:
            event.begin.time += timedelta(hours=1)
            event.end.time += timedelta(hours=1)
    with open(path, 'w', encoding='utf-8', newline='') as file:
        file.writelines(c.serialize_iter())
def testing(path: str):
    with open(path, 'r', newline='', encoding='utf-8') as file:
        c = Calendar(file.read())
    pass

if __name__ == "__main__":
    testing(r'C:\Users\yonat\Desktop\Code\Python\Personal_projects\Calander_gen\repo\Calander\classes.ics')