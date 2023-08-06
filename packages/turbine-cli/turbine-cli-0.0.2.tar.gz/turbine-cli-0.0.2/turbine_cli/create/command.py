import click
from cookiecutter.main import cookiecutter


@click.command('create')
@click.option('--project', '-p', 'project_name', prompt='Enter project name')
@click.option('--author', '-a', 'author', default='swimlane', prompt='Enter author name')
def create(project_name: str, author: str):
    """
    Create new project from cookie cutter template.
    :param project_name: Project name.
    :param author: Project author.
    :return: 0 if successful.
    """
    cookiecutter('https://github.com/swimlane/cookiecutter-turbine-bundle',
                 no_input=True,
                 extra_context={'project_name': project_name, 'author': author})
