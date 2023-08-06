# -*- coding: utf-8 -*-
"""commands.py is a module containing a collection of command implementations."""
import os

import blingrc

from .utils import try_subprocess_call
from .utils import stderr

from ..vendor import travis
from ..vendor import packer


def validate(config):
    validation = blingrc.validate_config(config)
    if not validation.has_error:
        return True
    else:
        [stderr(error) for error in validation.errors]
        return False


def start(config, is_build=False, image=None):
    if is_build:
        is_success = build(config)
        if not is_success:
            return False

    command = ['docker run'] + config['start']
    command = ' '.join(command)
    environ = {
        'NAME': config['name'], 'IMAGE': image or config['image']
    }
    environ = blingrc.patch_environ(environ, config['env'])
    return try_subprocess_call(command, environ=environ)


def stop(config):
    environ = blingrc.patch_environ(os.environ, config['env'])
    return try_subprocess_call(['docker', 'stop', config['name']], environ=environ)


def run(config):
    environ = blingrc.patch_environ(os.environ, config['env'])
    return try_subprocess_call(config['run'], environ=environ)


def build(config, should_publish=False, is_debug=False):
    command = packer.bootstrap_config(config, not should_publish, is_debug)

    environ = os.environ.copy()
    environ = travis.patch_environ(environ)
    environ = blingrc.patch_environ(environ, config['env'])

    is_success = try_subprocess_call(command, environ=environ)

    packer.cleanup_config()
    return is_success
