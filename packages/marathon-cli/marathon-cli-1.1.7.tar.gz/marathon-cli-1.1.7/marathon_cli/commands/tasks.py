import click
from pretty_json import format_json

from marathon_cli.utils import pickle_object
from marathon_cli.x import get


@click.command()
@click.option('-p', '--pickle', 'pickle_it', is_flag=True, help='pickle the response object and save it')
@click.pass_context
def cli(ctx, pickle_it):
    """Get all running tasks.
    """
    tasks = get('tasks')

    if pickle_it:
        pickle_object(tasks, 'tasks')

    click.echo(format_json(tasks.json()))
