import argparse
import os
import sys

from rope.base.project import Project
from rope.base.change import ChangeSet
from rope.base.resources import File
from rope.refactor.importutils import ImportOrganizer
from rope.refactor.wrap_line import WrapLine


class Agent(object):
    def __init__(self, target_file, dry_run):
        self.project = Project(os.getcwd())
        self.target_file = target_file
        self.dry_run = dry_run
        self.commands = []

    @property
    def resource(self):
        return File(self.project, self.target_file)

    def add_command_class(self, command_class):
        self.commands.append(command_class)

    def do(self):
        commands = [
            command_class(self.project, self.target_file, self.dry_run)
            for command_class in self.commands
        ]
        changesets = filter(
            lambda x: x is not None,
            [
                command.get_changeset()
                for command in commands
            ]
        )

        # merge changesets
        def merge_changesets(aggregated_changeset, next_changeset):
            for change in next_changeset.changes:
                aggregated_changeset.add_change(change)
            aggregated_changeset.description += next_changeset.description
            return aggregated_changeset

        new_changeset = reduce(
            merge_changesets,
            changesets,
            ChangeSet('')
        )

        if not new_changeset.changes:
            return

        if self.dry_run:
            print new_changeset.get_description()
        else:
            self.project.do(new_changeset)


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
    if not os.path.exists(target_file):
        print >> sys.stderr, "Target file doesn't exist"
        sys.exit(1)

    agent = Agent(target_file, args.dry_run)
    agent.add_command_class(OrganizeImportCommand)
    agent.add_command_class(WrapLineCommand)
    agent.do()
