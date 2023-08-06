import os
from os.path import join
import click
from turbine_cli.package import verify_project_folder
import requests


def upload_file(_file, url):
    """
    Uploads file to Turbine
    :param _file: File path
    :param url: Target Turbine url
    :return: None
    """
    with open(_file, 'rb') as stream:
        file_field = {'first_file': stream}
        result = requests.post(url, files=file_field)
        click.echo("{file} was sent, server returned {code}.".format(
            file=_file.split('/')[-1], code=result.status_code))


def get_url(turbine_api):
    """
    Get url. Instead of assuming it's just a server name, we can allow adding full url or
    sort of partial, in case we need to specify schema (http vs https)
    :param turbine_api: Server partial url
    :return: Full import api address
    """
    if turbine_api.startswith('http'):
        if 'import' in turbine_api:
            return turbine_api if turbine_api.endswith('/') else turbine_api + '/'
        else:
            return "{server}/api/import/".format(server=turbine_api)
    return "http://{server}/api/import/".format(server=turbine_api)


@click.command('upload')
@click.option('--project', '-p', 'project_folder', default='.', help='Project folder')
@click.option('--server', '-s', 'turbine_api', default='http://localhost:8080/api/import/',
              prompt='REST api address.',
              help='Turbine server REST api address.')
@click.option('--file', '-f',
              help='Specific file if only partial upload is required. Leave empty otherwise.')
def upload(project_folder, turbine_api, file=None):
    """
    Uploads zipped bundles and yml workflows to Turbine.
    :param project_folder: Project directory
    :param turbine_api: Turbine REST api address, server[port] or full one to import endpoint
    :param file: Single file when only one file needs to be uploaded
    :return: None
    """
    current_path = verify_project_folder(project_folder)
    url = get_url(turbine_api)

    if file:
        upload_file(file, url)
        return

    zip_file_folder = join(current_path, '_zip')
    for root, _, files in os.walk(zip_file_folder):
        for _file in files:
            if not _file.endswith('zip'):
                continue
            upload_file(join(root, _file), url)
        break

    dag_folder = join(current_path, '_playbook')
    for root, _, files in os.walk(dag_folder):
        for _file in files:
            if not _file.endswith('yml'):
                continue
            upload_file(join(root, _file), url)
        break