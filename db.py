# from collections import Counter
from typing import Counter

from datetime import datetime
from typing import Optional

from decouple import config
from sqlmodel import Field, SQLModel, create_engine, Session, select


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start: datetime
    end: Optional[datetime] = None

    @property
    def duration_in_seconds(self) -> int:
        if self.end is None:
            return 0
        return (self.end - self.start).seconds


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


def get_activities(name: Optional[str]) -> dict[str, int]:
    activities = Counter()

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


if __name__ == "__main__":
    create_tables()
