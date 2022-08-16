from datetime import datetime
from typing import Counter, Optional

from decouple import config
from sqlmodel import SQLModel, create_engine, Session, select

from model import Activity

db_url = config("DATABASE_URL")
debug = config("DEBUG", default=False)
engine = create_engine(db_url, echo=debug)


def create_tables():
    SQLModel.metadata.create_all(engine)


def add_activity(name: str) -> None:
    activity = Activity(
        name=name,
        start=datetime.now()
    )
    with Session(engine) as session:
        session.add(activity)
        session.commit()


def stop_activity(name: str) -> None:
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


def cancel_activity(name: str) -> None:
    with Session(engine) as session:
        statement = select(Activity).where(
            Activity.name == name,
            Activity.end == None  # noqa E711
        )
        results = session.exec(statement)
        for row in results:
            session.delete(row)
        session.commit()


def get_activities(name: Optional[str]) -> Counter[str]:
    activities: Counter[str] = Counter()

    with Session(engine) as session:
        statement = select(Activity)
        if name is not None:
            statement = statement.where(
                Activity.name == name,
            )
        results = session.exec(statement)
        for row in results:
            activities[row.name] += row.duration_in_seconds

    return activities


def remove_activities(name: str, all_entries: bool = False) -> None:
    with Session(engine) as session:
        statement = select(Activity).where(
            Activity.name == name,
        )

        results = session.exec(statement).all()
        if not all_entries:
            results = [results[-1]]

        for row in results:
            session.delete(row)
        session.commit()


if __name__ == "__main__":
    create_tables()
