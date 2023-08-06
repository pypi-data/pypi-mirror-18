#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bling.py

usage:
    bling
    bling start [--build] [--image=<image>]
    bling stop
    bling run
    bling validate
    bling build [--template=<template>]

commands:
    start                  starts app inside an interactive container
    stop                   stops running container
    run                    starts app inside a container, executing the specified run command
    validate               validates your `.bling.json` config file
    build                  invokes `packer build` with packer template json file

options:
    --build                forces packer to build a new docker image before starting
    --image=<image>        starts your container with a specified image
    --template=<template>  path to the packer template json file

    -h --help              shows this
    -v --version           shows version
"""
from . import __version__

from .core import blingrc
from .core import commands
from .core.utils import stderr, stdout

from .domain.blingrc import MissingBlingConfig
from .domain.blingrc import MalformedBlingConfig
from .domain.blingrc import InvalidBlingConfig

from docopt import docopt


def _parse_user_input(config, args):
    if args['start']:
        return commands.start(config, is_build=args['build'], image=args['--image'])
    if args['stop']:
        return commands.stop(config)
    if args['build']:
        return commands.build()
    if args['run']:
        return commands.run(config)
    if args['validate']:
        return commands.validate(config)
    return commands.start(config)


def main():
    args = docopt(__doc__, version=__version__)
    try:
        config = blingrc.open_config()
    except (MissingBlingConfig, MalformedBlingConfig, InvalidBlingConfig) as e:
        return stderr('bling err: %s' % e)
    try:
        _parse_user_input(config, args)
    except KeyboardInterrupt:
        return stdout('closing stdout, finished execution')
    exit(0)


if __name__ == '__main__':
    main()
