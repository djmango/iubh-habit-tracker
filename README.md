# Python Habit Tracker

This is a simple habit tracker written in Python. It is designed to be used from the command line.

## Description

This application utilizes Click to create a command line interface. Persistent storage is handled by pickling the HabitManager. The HabitManager is a list of Habit objects. Each Habit object has a name, a list of datetime objects indicating completions, a creation date, and a frequency. The HabitManager is pickled and stored in a file called `habits_manager.pkl`. The HabitManager is loaded from this file when the application is run.

## Getting Started

### Dependencies

* Python 3.10
* PIP

### Installing

* Clone the repository

```bash
git clone
```

* Install the requirements

```bash
pip install -r requirements.txt
```

### Executing program

```bash
python habit-tracker/cli.py --help
```

Examples:

To add a habit called "Exercise" that is completed every day:

```bash
python habit-tracker/cli.py habbit "Exercise" add --frequency "daily"
```

To list all habits and their streaks:

```bash
python habit-tracker/cli.py habits
```

## Authors

Sulaiman Ghori  
[@djmango](https://github.com/djmango)

## Version History

* 0.1
    * Initial Release
