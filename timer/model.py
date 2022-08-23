from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start: datetime
    end: Optional[datetime] = None

    @property
    def duration_in_minutes(self) -> float:
        if self.end is None:
            return 0
        minutes = (self.end - self.start).seconds / 60
        return minutes
