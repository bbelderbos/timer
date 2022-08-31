from datetime import datetime

import pytest

from timer.db import ActivityDb
from timer.exceptions import DuplicateTimerException


@pytest.fixture(scope="function")
def db():
    return ActivityDb(db_url="sqlite:///:memory:", create_tables=True)


def test_adding_activity_shows_one_act_in_transit(db):
    db.add_activity("read")
    assert db.get_number_of_activities_in_transit("read") == 1


def test_adding_activity_does_not_have_end_time(db):
    db.add_activity("code")
    act = db.get_last_activity("code")
    assert act.name == "code"
    assert isinstance(act.start, datetime)
    assert act.end is None


def test_stopping_activity_sets_end_time(db):
    db.add_activity("code")
    db.stop_activity("code")
    act = db.get_last_activity("code")
    assert isinstance(act.end, datetime)
    assert act.end > act.start


def test_cancel_activity_deletes_the_timer(db):
    db.add_activity("code")
    act = db.get_last_activity("code")
    assert act.name == "code"
    db.cancel_activity("code")
    act = db.get_last_activity("code")
    assert act is None


def test_should_not_be_able_to_start_unfinished_timer(db):
    db.add_activity("code")
    with pytest.raises(DuplicateTimerException):
        db.add_activity("code")
