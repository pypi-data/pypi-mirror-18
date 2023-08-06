# -*- coding: utf-8 -*-
import json
import os

from ..domain import blingrc
from ..domain.vendor import PackerConfigNotFound
from ..vendor.packer import read_config

CONFIG_FILE = os.path.abspath('./.bling.json')
REQUIRED_KEYS = [
    'run',
    'start',
    'name',
    'packer',
]
OPTIONAL_KEYS = {
    'env': {},
}


def open_config():
    try:
        with open(CONFIG_FILE, 'rU') as f:
            data = json.load(f)
        for key, default in OPTIONAL_KEYS.iteritems():
            if key not in data:
                data[key] = default
        return data
    except IOError:
        raise blingrc.MissingBlingConfig('cannot find "%s" config file' % CONFIG_FILE)
    except ValueError as e:
        raise blingrc.MalformedBlingConfig('malformed json in "%s"\n%s' % (CONFIG_FILE, e))


def validate_config(config):
    errors = []
    for key in REQUIRED_KEYS:
        if key in config.keys():
            continue
        errors.append('expected key: "%s" key (not found)' % key)
    try:
        read_config(config.get('packer', ''))
    except PackerConfigNotFound as e:
        errors.append('err: %s (packer missing)' % e)
    return blingrc.ConfigValidation(errors=errors, config=config)


def patch_environ(environ, config):
    environ = environ.copy()
    environ.update({k: str(v) for k, v in config.iteritems()})
    return environ
