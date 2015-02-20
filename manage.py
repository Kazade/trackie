#!/usr/bin/env python
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
APPENGINE_DIR = os.path.join(THIS_DIR, "third_party", "google_appengine")
DEVELOPMENT_DIR = os.path.join(THIS_DIR, "third_party", "local")

sys.path[0:0] = [
    os.path.join(THIS_DIR, 'src'),
    APPENGINE_DIR,
    DEVELOPMENT_DIR
]

from scaffold.boot import fix_path
fix_path()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scaffold.settings")

    from djangae.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
