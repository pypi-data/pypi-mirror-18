# -*- coding: utf-8 -*-
import json
import os

from blingtron.domain import blingrc

CONFIG_FILE = os.path.abspath('./.bling.json')
REQUIRED_KEYS = [
    'run',
    'start',
    'name',
    'image',
]


def open_config():
    try:
        with open(CONFIG_FILE, 'rU') as f:
            return json.load(f)
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
    return blingrc.ConfigValidation(errors=errors, config=config)
