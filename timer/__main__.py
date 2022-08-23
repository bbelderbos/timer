from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .db import (
    add_activity,
    cancel_activity,
    get_activities,
    get_number_of_activities_in_transit,
    remove_activities,
    stop_activity,
)

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


@app.command()
def start(name: str, interactive: bool = False):
    """
    Start timer for activity
    """
    num_activities = get_number_of_activities_in_transit(name)
    if num_activities > 0:
        err_console.print(
            f"Cannot start another activity for {name}, " f"{num_activities} in transit"
        )
        return
    add_activity(name)


@app.command()
def stop(name: str):
    """
    Stop timer for activity
    """
    num_activities = get_number_of_activities_in_transit(name)
    if num_activities == 0:
        err_console.print(f"Cannot stop activity {name}, nothing in transit")
        return
    stop_activity(name)


@app.command()
def cancel(name: str):
    """
    Cancel a timer for an activity in transit
    """
    num_activities = get_number_of_activities_in_transit(name)
    if num_activities == 0:
        err_console.print(f"Cannot cancel activity {name}, nothing in transit")
        return
    cancel_activity(name)


@app.command()
def show(name: Optional[str] = typer.Argument(None)):
    """
    Show timer for all activities or a specific activity
    """
    title = "Activities"
    if name is not None:
        title += f" ({name})"
    table = Table(title=title)

    table.add_column("Name", style="cyan")
    table.add_column("Total", style="magenta")

    activities = get_activities(name)
    for name, total in activities.items():
        table.add_row(name, str(total))

    console.print(table)


@app.command()
def remove(name: str, all_entries: bool = False):
    """
    Remove timer for an activity, last or all entries
    """
    print("remove", name, f"{all_entries=}")
    remove_activities(name, all_entries)


if __name__ == "__main__":
    app()
