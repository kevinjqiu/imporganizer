import argparse
import os
import sys

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

    if not os.path.exists(target_file):
        print >> sys.stderr, "Target file doesn't exist"
        sys.exit(1)

    project = Project(os.getcwd())
    import_organizer = ImportOrganizer(project)
    resource = File(project, target_file)
    changeset = import_organizer.organize_imports(resource)

    if changeset is not None:
        if args.dry_run:
            print changeset.get_description()
        else:
            project.do(changeset)
    else:
        print 'No changes'
