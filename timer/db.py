from collections import Counter
from datetime import datetime
from typing import Optional

from decouple import config
from sqlmodel import Session, SQLModel, create_engine, select

from .exceptions import DuplicateTimerException
from .model import Activity

debug = config("DEBUG", default=False)


class ActivityDb:
    def __init__(self, db_url=None, create_tables=False):
        if db_url is None:
            db_url = config("DATABASE_URL")
        self.engine = create_engine(db_url, echo=debug)
        if create_tables:
            self.create_tables()

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def add_activity(self, name: str) -> None:
        num_activities = self.get_number_of_activities_in_transit(name)
        if num_activities > 0:
            raise DuplicateTimerException
        activity = Activity(name=name, start=datetime.now())
        with Session(self.engine) as session:
            session.add(activity)
            session.commit()

    def get_last_activity(self, name: str) -> Activity:
        with Session(self.engine) as session:
            statement = (
                select(Activity)
                .where(Activity.name == name)
                .order_by(Activity.start.desc())
            )
            results = session.exec(statement)
            return results.first()

    def get_number_of_activities_in_transit(self, name: str) -> int:
        with Session(self.engine) as session:
            statement = select(Activity).where(
                Activity.name == name, Activity.end == None  # noqa E711
            )
            results = session.exec(statement)
            return len(results.fetchall())

    def stop_activity(self, name: str) -> None:
        with Session(self.engine) as session:
            statement = select(Activity).where(
                Activity.name == name, Activity.end == None  # noqa E711
            )
            results = session.exec(statement)
            for row in results:
                row.end = datetime.now()
                session.add(row)
            session.commit()

    def cancel_activity(self, name: str) -> None:
        with Session(self.engine) as session:
            statement = select(Activity).where(
                Activity.name == name, Activity.end == None  # noqa E711
            )
            results = session.exec(statement)
            for row in results:
                session.delete(row)
            session.commit()

    def get_activities(self, name: Optional[str]) -> Counter[str]:
        activities: Counter[str] = Counter()

        with Session(self.engine) as session:
            statement = select(Activity)
            if name is not None:
                statement = statement.where(
                    Activity.name == name,
                )
            results = session.exec(statement)
            for row in results:
                activities[row.name] += row.duration_in_seconds

        return activities

    def remove_activities(self, name: str, all_entries: bool = False) -> None:
        with Session(self.engine) as session:
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
    act_db = ActivityDb()
    act_db.create_tables()
