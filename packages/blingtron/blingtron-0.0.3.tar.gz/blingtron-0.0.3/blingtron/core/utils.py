# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import subprocess


def _format_subprocess_command(command):
    return ' '.join(command) if isinstance(command, list) else command


def try_subprocess_call_and_return(command, environ=None):
    try:
        env = os.environ.copy()
        env.update(environ or {})

        command = _format_subprocess_command(command)
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, env=env, shell=True
        )
        out, error = p.communicate()

        if p.returncode != 0:
            return False, error
        return True, out.strip('\n')
    except OSError as e:
        return False, e
    except subprocess.CalledProcessError as e:
        return False, e


def try_subprocess_call(command, environ=None):
    stdout('executing cmd: %s' % command)
    try:
        env = os.environ.copy()
        env.update(environ or {})

        command = _format_subprocess_command(command)
        subprocess.call([command], env=env, shell=True)
        return True
    except OSError as e:
        stderr('subprocess err: %s' % e)
        return False


def print_environ(environ):
    stdout('\n'.join(sorted(['%s=%s' % (k, v) for k, v in environ.iteritems()])))


def stdout(msg):
    print(msg, file=sys.stdout)


def stderr(msg):
    print(msg, file=sys.stderr)
