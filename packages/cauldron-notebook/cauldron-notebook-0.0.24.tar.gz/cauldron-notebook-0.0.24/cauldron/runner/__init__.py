import sys
import os
import glob
import importlib
import typing

import cauldron
from cauldron import environ
from cauldron.runner import source
from cauldron.session.projects import Project
from cauldron.session.projects import ProjectStep
from cauldron.environ import Response


def initialize(project: typing.Union[str, Project]):
    """

    :param project:
    :return:
    """

    if isinstance(project, str):
        project = Project(source_directory=project)

    sys.path.append(project.library_directory)

    cauldron.project.load(project)
    return project


def close():
    """

    :return:
    """

    os.chdir(os.path.expanduser('~'))
    project = cauldron.project.internal_project
    if not project:
        return False

    sys.path.remove(project.library_directory)
    cauldron.project.unload()
    return True


def reload_libraries():
    """
    Reload the libraries stored in the project's library directory
    :return:
    """

    project = cauldron.project.internal_project

    directory = project.library_directory
    glob_path = os.path.join(directory, '**', '*.py')
    for path in glob.glob(glob_path, recursive=True):
        package = path[len(directory) + 1:-3].replace(os.sep, '.')
        module = sys.modules.get(package)
        if module is not None:
            print('RELOADED:', package)
            importlib.reload(module)


def section(
        response: Response,
        project: typing.Union[Project, None],
        starting: ProjectStep = None,
        limit: int = 1,
        force: bool = False
) -> list:
    """

    :param response:
    :param project:
    :param starting:
    :param limit:
    :param force:
    :return:
    """

    limit = max(1, limit)

    if project is None:
        project = cauldron.project.internal_project

    starting_index = 0
    if starting:
        starting_index = project.steps.index(starting)
    count = 0

    steps_run = []

    for ps in project.steps:
        if count >= limit:
            break

        if ps.index < starting_index:
            continue

        if not force and count == 0 and not ps.is_dirty():
            continue

        steps_run.append(ps)
        if not source.run_step(response, project, ps, force=force):
            return steps_run

        count += 1

    return steps_run


def complete(
        response: Response,
        project: typing.Union[Project, None],
        starting: ProjectStep = None,
        force: bool = False,
        limit: int = -1
) -> list:
    """
    Runs the entire project, writes the results files, and returns the URL to
    the report file

    :param response:
    :param project:
    :param starting:
    :param force:
    :param limit:
    :return:
        Local URL to the report path
    """

    if project is None:
        project = cauldron.project.internal_project

    starting_index = 0
    if starting:
        starting_index = project.steps.index(starting)
    count = 0

    steps_run = []

    for ps in project.steps:
        if 0 < limit <= count:
            break

        if ps.index < starting_index:
            continue

        if not force and not ps.is_dirty():
            if limit < 1:
                environ.log(
                    '[{}]: Nothing to update'.format(ps.definition.name)
                )
            continue

        count += 1

        steps_run.append(ps)
        if not source.run_step(response, project, ps, force=True):
            return steps_run

    return steps_run

