import click
import habbit

habbit_manager = habbit.HabbitManager().load()

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo('Hello World!')
    # habbit_manager.save()

if __name__ == '__main__':
    cli()