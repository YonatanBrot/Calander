import typer
from ics import Event, Calendar
from arrow import Arrow

app = typer.Typer()

@app.command()
def add(items: list[str]):
    try:
        with open('events.ics', 'r') as file:
            c = Calendar(file)
            for item in items:
                date,name = item.split(';')
                date = [int(n) for n in date.split('/')]
                c.events.add(Event(name, Arrow(date[0], date[1], date[2])))
        with open('events.ics', 'w', encoding='utf-8', newline='') as file:
            file.writelines(c.serialize_iter())

    except FileNotFoundError:
        c = Calendar()
        date, name = items[0].split(';')
        date = [int(n) for n in date.split('/')]
        c.events.add(Event(name, Arrow(date[0], date[1], date[2])))
        with open('events.ics', 'w', newline='', encoding='utf-8') as file:
            file.writelines(c.serialize_iter())
        try:
            add(items[1:])
        except IndexError:
            pass

if __name__ == "__main__":
    app()