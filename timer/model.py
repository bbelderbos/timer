from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


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
