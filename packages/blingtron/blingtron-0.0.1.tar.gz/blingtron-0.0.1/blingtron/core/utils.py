# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from subprocess import call


def try_subprocess_call(command, environ=None):
    """Invokes `subprocess.call`, wrapping the OSError exception."""
    command = ' '.join(command)
    print('executing cmd:', command)

    try:
        env = os.environ.copy()
        env.update(environ or {})

        call([command], env=env, shell=True)
        return True
    except OSError as e:
        print(e)
        return False
