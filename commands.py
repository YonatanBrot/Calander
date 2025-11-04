import typer
from ics import Event, Calendar
from arrow import Arrow
import datetime as dt

app = typer.Typer()

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

if __name__ == "__main__":
    app()