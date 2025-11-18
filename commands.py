import typer
from ics import Event, Calendar
from ics.grammar.parse import ContentLine
import arrow as aw
import datetime as dt

app = typer.Typer()

@app.command()
def move(path: str, offset: int):
    print(path)
    with open(path, 'r', encoding='utf-8') as file:
        c = Calendar(file.read())
    for e in c.events:
        e.end = e.end.shift(hours=offset)
        e.begin = e.begin.shift(hours=offset)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        file.writelines(c.serialize_iter())

@app.command()
def blackout(dates: list[str]):
    abs_dates = []
    for date in dates:
        try:
            abs_dates.append((aw.get(date[:10]),aw.get(date[10:])))
        except IndexError:
            abs_dates.append(aw.get(date))
    

# def add(path:str, begin:str, end:str, name:str, location:str, rrules:list[str]):
#     e = Event(name, aw.get(begin), aw.get(end), location=location)
#     for r in rrules:
#         e.extra.append(ContentLine('RRULE', value=r))
#     try:
#         with open(path, 'r', encoding='utf-8') as file:
#             c = Calendar(file.read())
#     except FileNotFoundError:
#         c = Calendar(creator='-//YB/classes//EN')
#     c.events.add(e)
#     with open(path, 'w', encoding='utf-8', newline='') as file:
#         file.writelines(c.serialize_iter())

# def combine(path:str):
#     with open(path, 'r', encoding='utf-8') as file:
#         c = Calendar(file.read())
#     c.events = tuple(c.events)
    
#     for i in range(len(c.events)):

@app.command()
def addAllDay(path:str, events:list[str]):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            c = Calendar(file.read())
    except:
        c = Calendar()
    for event in events:
        event = Event(event[:-8], event[-8:])
        event.make_all_day()
        c.events.add(event)
    with open(path, 'w', encoding='utf-8', newline='') as file:
        file.writelines(c.serialize_iter())
        


    


                

if __name__ == "__main__":
    app()