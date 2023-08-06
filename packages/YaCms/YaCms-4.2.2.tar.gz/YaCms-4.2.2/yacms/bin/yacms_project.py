#!/usr/bin/env python
import sys

from django.conf import settings
from django.core import management


def create_project():
    # Put yacms.conf in INSTALLED_APPS so call_command can find
    # our command,
    settings.configure()
    settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + ['yacms.bin']
    argv = sys.argv[:1] + ['yacms_project'] + sys.argv[1:]
    management.execute_from_command_line(argv)


if __name__ == "__main__":
    create_project()
