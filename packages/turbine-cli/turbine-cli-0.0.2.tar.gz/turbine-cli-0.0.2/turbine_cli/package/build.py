import os
import zipfile
from os import mkdir
from os.path import relpath, join, dirname, basename, exists
import click
import yaml
from turbine.schema.validate import validate_file
from turbine_cli.package import BuildError, verify_project_folder


def zip_dir(path, zip_file):
    """
    Generic zip contents of a directory. Only one level deep.
    :param path: Directory path
    :param zip_file: Zip file to put content into
    :return: None
    """
    for root, _, files in os.walk(path):
        for file in files:
            if file.startswith('.'):
                continue
            zip_file.write(join(root, file), relpath(join(root, file), path))


def get_package_name(path):
    """
    Get the package name based on bundle config or name of the directory.
    :param path: Bundle directory path
    :return: Name
    """
    config_file = os.path.join(path, 'config/bundle.yml')
    if os.path.isfile(config_file):
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)
            return config['name']
    else:
        return basename(path)


def validate_config(folder):
    """
    Validate configuration files against the schema.
    :param folder: Bundle directory
    :return: None
    :except: BuildError
    """
    config_folder = join(folder, 'config')
    if not exists(config_folder):
        raise BuildError("Configuration is not found. Possibly folder is not bundle folder?")

    for root, _, files in os.walk(config_folder):
        for file in files:
            validate_file(join(root, file))
        break


def validate(folder):
    """
    Generic method to validate bundle.
    :param folder: Bundle directory
    :return: None
    """
    validate_config(folder)


@click.command('build')
@click.option('--project', '-p', 'project_folder', default='.',
              help='Project folder if not same folder.')
def build(project_folder):
    """
    Build the bundles in the project. One or many.
    :param project_folder: Project directory
    :return: None
    """
    try:
        current_path = verify_project_folder(project_folder)
        for root, folders, _ in os.walk(current_path):
            for _folder in folders:
                if _folder.startswith('.') or _folder.startswith('_'):
                    continue
                package_folder = join(root, _folder)
                validate(package_folder)
                package_name = get_package_name(package_folder)
                zip_file_name = join(current_path, '_zip', (package_name + '.zip'))
                if not exists(dirname(zip_file_name)):
                    mkdir(dirname(zip_file_name))
                _zip_file = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
                zip_dir(package_folder, _zip_file)
                _zip_file.close()
            break
    except BuildError as e:
        click.echo(e)
