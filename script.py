from typing import Optional

from sqlmodel.sql.expression import Select, SelectOfScalar
import typer

from db import (
    add_activity, stop_activity, cancel_activity,
    get_activities, remove_activities)

# https://github.com/tiangolo/sqlmodel/issues/189
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
    remove_activities(name, all_entries)


if __name__ == "__main__":
    app()
