from datetime import datetime
from typing import Optional

from decouple import config
from sqlmodel import Field, SQLModel, create_engine


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start: datetime
    end: Optional[datetime] = None


db_url = config("DATABASE_URL")
engine = create_engine(db_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
