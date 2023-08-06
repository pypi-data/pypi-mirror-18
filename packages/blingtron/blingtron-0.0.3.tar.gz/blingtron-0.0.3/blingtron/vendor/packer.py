# -*- coding: utf-8 -*-
import os
import json
import shutil

from ..domain.vendor import PackerConfigNotFound

PUBLISH_TYPES = [
    'docker-push',
]

PACKER_TMP_ROOT = os.path.abspath('./.bling')
PACKER_TMP_PATH = os.path.join(PACKER_TMP_ROOT, 'template.updated.json')


def read_config(path):
    abs_path = os.path.abspath(path)
    try:
        with open(abs_path, 'rU') as f:
            packer_template = json.load(f)
    except IOError:
        raise PackerConfigNotFound('cannot open "%s"' % abs_path)
    return packer_template


def write_config(config, destination):
    dirname = os.path.dirname(destination)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(destination, 'w') as f:
        json.dump(config, f, indent=2, sort_keys=True)
    return destination


def remove_publish_processes(packer_path, publish_types):
    packer_template = read_config(packer_path)
    if 'post-processors' not in packer_template:
        return packer_path

    post_processes = []
    for processes in packer_template['post-processors']:
        processes = [p for p in processes if p['type'] not in publish_types]
        post_processes.append(processes)
    packer_template['post-processors'] = post_processes
    return write_config(packer_template, PACKER_TMP_PATH)


def bootstrap_config(config, remove_publish=False, is_debug=False):
    command = ['packer', 'build']
    if is_debug:
        command.append('-debug')
    if remove_publish:
        packer_template_path = remove_publish_processes(config['packer'], PUBLISH_TYPES)
        command.append(packer_template_path)
    else:
        command.append(config['packer'])
    return command


def cleanup_config():
    if os.path.exists(PACKER_TMP_PATH):
        shutil.rmtree(PACKER_TMP_ROOT)
