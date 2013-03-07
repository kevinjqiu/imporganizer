import argparse
import os

from rope.base.project import Project
from rope.base.resources import File
from rope.refactor.importutils import ImportOrganizer
from rope.refactor.wrap_line import WrapLine


class Command(object):
    def __init__(self, project, target_file, dry_run):
        self.project = project
        self.target_file = target_file
        self.dry_run = dry_run

    @property
    def resource(self):
        return File(self.project, self.target_file)

    def __call__(self):
        changeset = self.get_changeset()
        if changeset is not None:
            if self.dry_run:
                print changeset.get_description()
            else:
                self.project.do(changeset)

    def get_changeset(self):
        raise NotImplementedError


class OrganizeImportCommand(Command):
    def get_changeset(self):
        import_organizer = ImportOrganizer(self.project)
        return import_organizer.organize_imports(self.resource)


class WrapLineCommand(Command):
    def get_changeset(self):
        line_wrapper = WrapLine(self.project, self.resource)
        return line_wrapper.get_changes()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dry-run', dest='dry_run', action='store_true',
        help='If set, only preview the changes',
    )
    parser.add_argument('target')
    args = parser.parse_args()

    target_file = args.target
    project = Project(os.getcwd())

    OrganizeImportCommand(project, target_file, args.dry_run)()
    WrapLineCommand(project, target_file, args.dry_run)()
