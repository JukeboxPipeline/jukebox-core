#!/usr/bin/env python
"""
Custom install command for tox when developing on several jukebox projects at the same time.
This will simply execute a localtoxinstall script where you can install dependencies in develop mode.
"""
from __future__ import print_function

import os
import sys
import subprocess


def start_process(args):
    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print(p.communicate())
    rc = p.poll()
    if rc:
        print('Process returncode: %s for args %s' % (rc, args), file=sys.stderr)
        sys.exit(rc)

script = os.path.join(os.path.dirname(__file__), 'localtoxinstall')
if not os.path.exists(script):
    print('localtoxinstall script not found. Create a localtoxinstall script file \
in the project dir. Have a look at the template for more information. \
Do not put the localtoxinstall script under version control!')
    sys.exit(1)

args = ['sh', script]
start_process(args)

args = ['pip', 'install', '--pre']
args.extend(sys.argv[1:])
start_process(args)
