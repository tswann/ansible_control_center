#!/usr/bin/env python

import sys
import os

HELP_TEXT = """
Usage: ./create_playbook.py /path/to/playbookname [role1 role2 ...]
Creates an empy playbook skeleton, with any roles that are specified.

e.g. ./create_playbook.py /tmp/pyplaybook web db cache
"""

def main():
    args = sys.argv
    if len(args) < 2:
        print('Invalid invocation. Exiting.')
        print(HELP_TEXT)
        sys.exit(1)

    playbook_location = args[1]
    roles_to_create = args[2:]

    if playbook_location in {'help', '-h', '--help'}:
        print(HELP_TEXT)
        sys.exit(0)
    else:
        playbook_location = os.path.abspath(playbook_location)

    if os.path.isdir(playbook_location) or os.path.isfile(playbook_location):
        print("Can't create a playbook with this path: something already exists there!")
        sys.exit(1)

    print('Creating playbook skeleton')
    create_playbook(playbook_location)

    for r in roles_to_create:
        print('Creating role: ', r)
        create_role(playbook_location, r)

def create_playbook(location):
    dirs_to_create = [
        "group_vars",
        "roles"
    ]

    files_to_create = [
        os.path.join("group_vars", "all"),
        "playbook.yml"
    ]

    print('Creating playbook directories')
    os.mkdir(location, 0755)
    for d in dirs_to_create:
        os.mkdir(os.path.join(location, d), 0755)

    print('Creating playbook files')
    for f in files_to_create:
        open(os.path.join(location, f), 'a').close()

def create_role(location, rolename):
    role_path_components = (location, "roles", rolename)
    dirs = ("tasks", "handlers", "templates", "files", "vars", "meta")

    dirs_to_create = [ 
        os.path.join(*role_path_components + (dir,)) for dir in dirs
    ]

    files_to_create = [
        os.path.join(*role_path_components + ("tasks", "main.yml")),
        os.path.join(*role_path_components + ("handlers", "main.yml"))
    ]

    print('Creating role directories')
    for d in dirs_to_create:
        os.makedirs(d, 0755)

    print('Creating role files')
    for f in files_to_create:
        open(f, 'a').close()

main()
