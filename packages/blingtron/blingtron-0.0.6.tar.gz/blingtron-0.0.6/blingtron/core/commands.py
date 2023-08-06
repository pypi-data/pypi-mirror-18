# -*- coding: utf-8 -*-
import os

import blingrc

from .utils import try_subprocess_call
from .utils import stderr
from .lock import write_lock

from ..vendor import travis
from ..vendor import packer
from ..vendor import docker


def validate(config):
    validation = blingrc.validate_config(config)
    if not validation.has_error:
        return True
    else:
        [stderr(error) for error in validation.errors]
        return False


def start(config):
    if packer.is_packer_updated(config['packer']):
        stderr('packer config has changed, re-run bling build')
        return False

    image_name = docker.get_image('{registry}/{name}'.format(**config))
    if not image_name:
        stderr('docker image for "%s" does not exist, run bling build' % image_name)
        return False

    write_lock(config['packer'])

    command = config['start'] + ['--name', config['name'], image_name, '/bin/bash']
    environ = blingrc.patch_environ(os.environ, config['env'])
    return docker.run(command, environ)


def stop(config):
    return docker.stop(config['name'])


def run(config):
    environ = blingrc.patch_environ(os.environ, config['env'])
    return try_subprocess_call(config['run'], environ=environ)


def build(config, should_publish=False, is_debug=False):
    command = packer.bootstrap_config(config, not should_publish, is_debug)

    environ = travis.patch_environ(os.environ)
    environ = blingrc.patch_environ(environ, config['env'])

    is_success = try_subprocess_call(command, environ=environ)

    packer.cleanup_config()
    write_lock(config['packer'])
    return is_success
