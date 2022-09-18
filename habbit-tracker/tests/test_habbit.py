import pytest
import datetime
import habbit

def test_habbit_mark_complete():
    h = habbit.Habbit('Test Habbit')
    h.mark_complete()
    assert h.completed_today()

def test_habbit_mark_incomplete():
    h = habbit.Habbit('Test Habbit')
    h.mark_complete()
    h.mark_incomplete()
    assert not h.completed_today()

def test_habbit_streak_length():
    h = habbit.Habbit('Test Habbit')
    h.created = datetime.datetime.now() - datetime.timedelta(days=5)
    h.mark_complete()
    assert h.streak_length() == 1

def test_habbit_streak_longest():
    h = habbit.Habbit('Test Habbit')
    h.mark_complete()
    assert h.streak_longest() == 1

def test_habbit_manager_save():
    hm = habbit.HabbitManager()
    hm.save()
    assert True
