import click
from cli.cli import pass_context

@click.command('intersect', short_help='Intersect with CSV file.')
@pass_context
def cli(ctx):
    """Shows file changes in the current working directory."""
    ctx.log('Intersect with CSV files: none')
    ctx.vlog('bla bla bla, debug info')