import pytest
import datetime
import habit

def test_habit_mark_complete():
    h = habit.Habit('Test Habit')
    h.mark_complete()
    assert h.completed_today()

def test_habit_mark_incomplete():
    h = habit.Habit('Test Habit')
    h.mark_complete()
    h.mark_incomplete()
    assert not h.completed_today()

def test_habit_streak_length():
    h = habit.Habit('Test Habit')
    h.created = datetime.datetime.now() - datetime.timedelta(days=5)
    h.mark_complete()
    assert h.streak_length() == 1

def test_habit_streak_longest():
    h = habit.Habit('Test Habit')
    h.mark_complete()
    assert h.streak_longest() == 1

def test_habit_manager_save():
    hm = habit.HabitManager()
    hm.save()
    assert True
