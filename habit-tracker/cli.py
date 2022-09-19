import click
import habit

habit_manager = habit.HabitManager().load()

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo('Hello World!')
    # habit_manager.save()

if __name__ == '__main__':
    cli()