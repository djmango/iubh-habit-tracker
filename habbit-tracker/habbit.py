""" Class and methods relating to the basic habbit object """

from pathlib import Path
import datetime
import pickle
from enum import Enum

import pandas as pd

HERE = Path(__file__).parent

class Frequency(Enum):
    DAILY = 'd'
    WEEKLY = 'w'

class Habbit:
    def __init__(self, name: str, frequency: Frequency = Frequency.DAILY):
        # Validation
        assert frequency in Frequency, f'{frequency} is not a valid frequency: {Frequency.__members__}'

        # Assignment 
        self.name = name
        self.frequency = frequency

        # Default values
        self.created = datetime.datetime.now()
        self.completed_times: list[datetime.datetime] = [] # List of datetime objects, indicating the completion history of a habbit

    def mark_complete(self):
        """ Marks the habbit as complete for today """
        self.completed_times.append(datetime.datetime.now())

    def mark_incomplete(self):
        """ Removes the most recent completion time """
        self.completed_times.pop()

    def completed_today(self):
        """ Returns True if the habbit has been completed today, False otherwise. """
        if not self.completed_times:
            return False
        else:
            return self.completed_times[-1].date() == datetime.datetime.now().date()
        
    def completed_on(self, date: datetime.date):
        """ Returns True if the habbit has been completed on the given date based on frequency, False otherwise. """
        assert type(date) == datetime.date, f'{date} is not a datetime.date object'

        for completion in self.completed_times:
            if self.frequency == Frequency.DAILY:
                if completion.date() == date:
                    return True
            elif self.frequency == Frequency.WEEKLY:
                if completion.date().isocalendar()[1] == date.isocalendar()[1]:
                    return True
        return False

    def streak_length(self):
        """ Returns the number of days in a row the habbit has been completed. """
        if not self.completed_times:
            return 0
        else:
            if self.completed_today(): # Daterange does not include today so this is just an easy fix alternatie being adding a day to the daterange
                streak = 1
            else:
                streak = 0

            daterange = pd.date_range(self.created, datetime.datetime.now().date())
            # iterate backwards over all days from today to created, breaking when a day is not completed
            for date in daterange[::-1]:
                if self.completed_on(date.date()):
                    streak += 1
                else:
                    break
            return streak

    def streak_longest(self):
        """ Returns length of the historically longest streak for the habbit """
        if not self.completed_times:
            return 0
        else:
            if self.completed_today(): # Daterange does not include today so this is just an easy fix alternatie being adding a day to the daterange
                streak = 1
            else:
                streak = 0
            streak_longest = streak

            daterange = pd.date_range(self.created, datetime.datetime.now().date())
            for date in daterange:
                if self.completed_on(date):
                    streak += 1
                else:
                    if streak > streak_longest:
                        streak_longest = streak
                    streak = 0
            return streak_longest


class HabbitManager:
    def __init__(self):
        self.habbits: list[Habbit] = []

    def save(self):
        pickle.dump(self, open(HERE/'data'/'habbit_manager.pkl', 'wb'))

    def load(self):
        if (HERE/'habbit_manager.pkl').exists():
            return pickle.load(open(HERE/'data'/'habbit_manager.pkl', 'rb'))
        else:
            return self

    def add_habbit(self, habbit: Habbit):
        self.habbits.append(habbit)
    
    def delete_habbit(self, habbit: Habbit):
        self.habbits.remove(habbit)

    def get_habbits(self):
        return self.habbits

    def get_habbits_by_frequency(self, frequency: Frequency):
        assert frequency in Frequency, f'{frequency} is not a valid frequency: {Frequency.__members__}'
        return [habbit for habbit in self.habbits if habbit.frequency == frequency]
    
    def get_habbit_streaks_longest(self):
        """ Returns a list of tuples containing the habbit name and its streak length, sorted by longest streak first. """
        streaks = [(habbit.name, habbit.streak_longest()) for habbit in self.habbits]
        streaks_sorted = sorted(streaks, key=lambda x: x[1], reverse=True)
        return streaks_sorted