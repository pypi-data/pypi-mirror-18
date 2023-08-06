import click
from turbine_cli.create.command import create
from turbine_cli.package.build import build
from turbine_cli.package.upload import upload


@click.group(chain=True)
@click.option('--log', '-l', default=False, is_flag=True, help='Log output to ./turbine-cli.log.')
@click.pass_context
def entry_point(ctx, log):
    ctx.obj = {'log': log}


entry_point.add_command(create)
entry_point.add_command(build)
entry_point.add_command(upload)
