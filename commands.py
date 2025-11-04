import typer
from ics import Event, Calendar
from arrow import Arrow
import datetime as dt

app = typer.Typer()

@app.command()
def add(path: str, args: list[str]):
    try:
        with open(path, 'r') as file:
            c = Calendar(file)
            for item in args:
                date,name = item.split(';')
                date = [int(n) for n in date.split('/')]
                c.events.add(Event(name, Arrow(date[0], date[1], date[2])))
        with open(path, 'w', encoding='utf-8', newline='') as file:
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
        begin = dt.date(begin[2], begin[1], begin[0])
        end = [int(n) for n in end.split('/')]
        end = dt.date(end[2], end[1], end[0])
        current = begin
        toReturn = [begin]
        while(current!=end):
            current+=dt.timedelta(1)
            toReturn.append(current)
        return toReturn
    else:
        time = [int(n) for n in string.split('/')]
        return [dt.date(time[2], time[1], time[0])]
            
@app.command()
def remove(path: str, args: list[str]):
    for item in args:
        with open(path, 'r') as file:
            c = Calendar(file)
        try:
            date,name = item.split(';')
            date = [int(n) for n in date.split('/')]
            c.events.remove(Event(name, Arrow(date[0], date[1], date[2])))
            with open(path, 'w', newline='', encoding='utf-8') as file:
                file.writelines(c.serialize_iter)
        except KeyError:
            print('Event not in calendar')

@app.command()
def blackout(args: list[str]):
    with open('classes.ics', 'r') as file:
        c = Calendar(file)
    dates = [str_to_date(i) for i in args]
    
@app.command()
def move(path: str, offset: int):
    print(path)
    with open(path, 'r', newline='', encoding='utf-8') as file:
        c = Calendar(file.read())
    for e in c.events:
        e.end = e.end.shift(hours=offset)
        e.begin = e.begin.shift(hours=offset)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        file.writelines(c.serialize_iter())


def testing(path: str):
    with open(path, 'r', newline='', encoding='utf-8') as file:
        c = Calendar(file.read())
    pass

if __name__ == "__main__":
    app()