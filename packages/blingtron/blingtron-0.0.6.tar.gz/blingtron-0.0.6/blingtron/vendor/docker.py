# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..core.utils import try_subprocess_call

import docker

DEFAULT_LOCAL_TAG = 'local'
_client = docker.from_env()


def run(arguments, environ):
    command = ['docker', 'run'] + arguments
    command = ' '.join(command)
    return try_subprocess_call(command, environ=environ)


def stop(container_name):
    _client.stop(container_name)
    return True


def get_image(name, tag=DEFAULT_LOCAL_TAG):
    image_name = '{name}:{tag}'.format(name=name, tag=tag)
    image_list = _client.images()
    found_image = [i for i in image_list if i['RepoTags'] == [image_name]]

    image = next(iter(found_image), None)
    return image_name if image else None
