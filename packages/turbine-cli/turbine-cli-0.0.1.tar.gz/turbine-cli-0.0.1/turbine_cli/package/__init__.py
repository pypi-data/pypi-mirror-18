from os.path import realpath, exists


class BuildError(Exception):
    pass


def verify_project_folder(project_folder):
    if project_folder != '.':
        if not exists(project_folder):
            raise BuildError("Project of that name was not found in this directory.")
    return realpath(project_folder)