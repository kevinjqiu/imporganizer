import argparse
import os

from rope.base.project import Project
from rope.base.resources import File
from rope.refactor.importutils import ImportOrganizer


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
    import_organizer = ImportOrganizer(project)
    resource = File(project, target_file)
    changeset = import_organizer.organize_imports(resource)

    if args.dry_run:
        print changeset.get_description()
    else:
        project.do(changeset)
