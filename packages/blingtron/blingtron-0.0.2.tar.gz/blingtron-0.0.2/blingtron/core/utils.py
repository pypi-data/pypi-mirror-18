# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
from subprocess import call


def try_subprocess_call(command, environ=None):
    """Invokes `subprocess.call`, wrapping the OSError exception."""
    command = ' '.join(command) if isinstance(command, list) else command
    stdout('executing cmd: %s' % command)
    try:
        env = os.environ.copy()
        env.update(environ or {})

        call([command], env=env, shell=True)
        return True
    except OSError as e:
        stderr('subprocess err: %s' % e)
        return False


def stdout(msg):
    print(msg, file=sys.stdout)


def stderr(msg):
    print(msg, file=sys.stderr)
