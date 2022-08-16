from collections import Counter
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
from sqlmodel.sql.expression import Select, SelectOfScalar
import typer

from db import Activity, engine, add_activity, stop_activity, cancel_activity, get_activities

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

app = typer.Typer()


@app.command()
def start(name: str, interactive: bool = False):
    """
    Start timer for activity
    """
    add_activity(name)


@app.command()
def stop(name: str):
    """
    Stop timer for activity
    """
    stop_activity(name)


@app.command()
def cancel(name: str):
    """
    Cancel a timer for an activity in transit
    """
    print("cancel", name)
    cancel_activity(name)


@app.command()
def show(name: Optional[str] = typer.Argument(None)):
    """
    Show timer for all activities or a specific activity
    """
    print("show", name)
    activities = get_activities(name)
    for name, total in activities.items():
        print(name, total)


@app.command()
def remove(name: str, all_entries: bool = False):
    """
    Remove timer for an activity, last or all entries
    """
    print("remove", name, f"{all_entries=}")
    with Session(engine) as session:
        statement = select(Activity).where(
            Activity.name == name,
        )

        results = session.exec(statement)
        if not all_entries:
            results = [results[-1]]

        for row in results:
            session.delete(row)
        session.commit()


if __name__ == "__main__":
    app()
