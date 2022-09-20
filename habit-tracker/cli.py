import click
from habit import Habit, HabitManager, Frequency

habit_manager = HabitManager().load()

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo('Hello World!')

# Habit manager commands
@cli.command()
@click.option('--frequency', default=None, type=click.Choice([f.name.lower() for f in Frequency]))
def habits(frequency: str):
    """ Lists all habits """
    click.echo(f'{len(habit_manager.get_habits())} Total Habits:')

    if frequency:
        habits = habit_manager.get_habits_by_frequency(Frequency[frequency.upper()])
        click.echo(f'{len(habits)} Habits with frequency {frequency}:')
    else:
        habits = habit_manager.get_habits()

    for habit in habits:
        click.echo(f'  {habit.name}')

@cli.command()
def streaks():
    """ Lists all habits with their streaks """
    click.echo(f'{len(habit_manager.get_habits())} Total Habits:')

    for habit in habit_manager.get_habits():
        click.echo(f'  {habit.name}: {habit.streak_length()}')

# Individual habit commands

# First we need to get a habit object to operate on
@cli.group()
@click.argument('name')
@click.pass_context
def habit(ctx, name):
    """ Commands for individual habits """
    # Populate context with habit if it exists
    ctx.obj = {}
    ctx.obj['name'] = name
    ctx.obj['habit'] = habit_manager.get_habit_by_name(name)

    # If it doesn't, prompt creation
    if not ctx.obj['habit'] and ctx.invoked_subcommand != 'create':
        create = click.prompt(click.style(f'Habit "{name}" does not exist. ', fg='yellow') + 'Create it?', type=click.Choice(['y', 'n']), default='n')
        if create == 'y':
            frequency = click.prompt('Frequency: ', type=click.Choice([f.name.lower() for f in Frequency]), default='daily')
            ctx.obj['habit'] = Habit(name, Frequency[frequency.upper()])
            habit_manager.add_habit(ctx.obj['habit'])
            click.echo(f'Habit "{name}" created.')

# Now we can define subcommands to operate upon the habit
@habit.command()
@click.pass_context
def info(ctx):
    """ Prints information about the habit """
    habit: Habit = ctx.obj['habit']
    click.echo(f'Name: {habit.name}')
    click.echo(f'Created: {habit.created.strftime("%Y-%m-%d %H:%M:%S")}')
    click.echo(f'Completed today: {habit.completed_today()}')
    click.echo(f'Streak: {habit.streak_length()}')
    click.echo(f'Longest Streak: {habit.streak_longest()}')

@habit.command()
@click.pass_context
def create(ctx):
    """ Create a new habit """
    habit: Habit = ctx.obj['habit']
    if habit:
        click.secho(f'Habbit {habit.name} already exists', fg='red')
    else:
        click.echo('Creating habit:')
        frequency = click.prompt('Frequency: ', type=click.Choice([f.name.lower() for f in Frequency]), default='daily')
        ctx.obj['habit'] = Habit(ctx.obj['name'], Frequency[frequency.upper()])
        habit_manager.add_habit(ctx.obj['habit'])
        click.secho(f'Habit "{ctx.obj["name"]}" created.', fg='green')

@habit.command()
@click.pass_context
def delete(ctx):
    """ Delete a habit """
    habit: Habit = ctx.obj['habit']
    habit_manager.delete_habit(habit)
    click.secho(f'Habit "{habit.name}" deleted.', fg='red')

@habit.command()
@click.pass_context
def complete(ctx):
    """ Mark habit as completed for today """
    habit: Habit = ctx.obj['habit']
    habit.mark_complete()
    habit_manager.save()
    click.secho(f'Habit "{habit.name}" marked as completed.', fg='green')

@habit.command()
@click.pass_context
def incomplete(ctx):
    """ Mark a habit as incomplete """
    habit: Habit = ctx.obj['habit']
    habit.mark_incomplete()
    habit_manager.save()
    click.secho(f'Habit "{habit.name}" marked as incompleted.', fg='red')

@habit.command()
@click.pass_context
def streak(ctx):
    """ Print the current streak """
    habit: Habit = ctx.obj['habit']
    click.echo(f'Streak: {habit.streak_length()} days')

@habit.command()
@click.pass_context
def longest_streak(ctx):
    """ Print the longest streak """
    habit: Habit = ctx.obj['habit']
    click.echo(f'Longest streak: {habit.streak_longest()} days')

if __name__ == '__main__':
    cli()