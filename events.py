import typer
from ics import Event, Calendar
from arrow import Arrow

app = typer.Typer()

@app.command()
def add(name: str, start: str, end:str):
    with open('events.py', 'r', encoding='utf-8', newline='') as file:
        pass
    
@app.command
def test(num: int):
    print(num+1)

@app.command()
def init(name: str, date: str):
    name = name.replace('_', ' ')
    date = [int(n) for n in date.strip().split('/')]
    c = Calendar(events = [Event(name = name, begin = Arrow(date[2], date[1], date[0]))], creator='-//YB/classes//EN')
    with open('events.ics', 'w', encoding='utf-8', newline='') as file:
        file.writelines(c.serialize_iter())

if __name__ == "__main__":
    app()