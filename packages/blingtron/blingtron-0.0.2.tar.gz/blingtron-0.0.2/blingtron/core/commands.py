# -*- coding: utf-8 -*-
from .blingrc import validate_config
from .utils import try_subprocess_call
from .utils import stderr, stdout


def validate(config):
    validation = validate_config(config)
    if not validation.has_error:
        stdout('success! bling config is valid')
        return True
    [stderr(error) for error in validation.errors]
    return False


def start(config, is_build=False, image=None):
    command = ['docker run'] + config['start']
    command = ' '.join(command)
    environ = {
        'NAME': config['name'], 'IMAGE': image or config['image']
    }
    return try_subprocess_call(command, environ)


def stop(config):
    return try_subprocess_call(['docker', 'stop', config['name']])


def run(config):
    return try_subprocess_call(config['run'])


def build(tag=None):
    return try_subprocess_call(['packer', 'build', 'packer/template.json'])
