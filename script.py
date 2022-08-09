from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
import typer

from db import Activity, engine

app = typer.Typer()


@app.command()
def start(name: str, interactive: bool = False):
    """
    Start timer for activity
    """
    activity = Activity(
        name=name,
        start=datetime.now()
    )
    with Session(engine) as session:
        session.add(activity)
        session.commit()


@app.command()
def stop(name: str):
    """
    Stop timer for activity
    """
    with Session(engine) as session:
        statement = select(Activity).where(
            Activity.name == name,
            Activity.end == None  # noqa E711
        )
        results = session.exec(statement)
        for row in results:
            row.end = datetime.now()
            session.add(row)
        session.commit()


@app.command()
def cancel(name: str):
    """
    Cancel a timer for an activity in transit
    """
    print("cancel", name)


@app.command()
def show(name: Optional[str] = typer.Argument(None)):
    """
    Show timer for all activities or a specific activity
    """
    print("show", name)


@app.command()
def remove(name: str, all_entries: bool = False):
    """
    Remove timer for an activity, last or all entries
    """
    print("remove", name, f"{all_entries=}")


if __name__ == "__main__":
    app()
