# -*- coding: utf-8 -*-
import os
import json
import shutil

from ..core.lock import md5sum_dir
from ..core.lock import read_lock
from ..domain.vendor import PackerConfigNotFound

from .docker import DEFAULT_LOCAL_TAG

PUBLISH_TYPES = [
    'docker-push',
]

PACKER_TMP_ROOT = os.path.abspath('./.bling')
PACKER_TMP_PATH = os.path.join(PACKER_TMP_ROOT, 'template.updated.json')
PACKER_CONFIG_FILE = 'template.json'


def is_packer_updated(packer_dir):
    old_hash = read_lock()
    new_hash = md5sum_dir(packer_dir)
    return old_hash and old_hash != new_hash


def read_config(path):
    path = os.path.join(path, PACKER_CONFIG_FILE)
    path = os.path.abspath(path)
    try:
        with open(path, 'rU') as f:
            packer_template = json.load(f)
    except IOError:
        raise PackerConfigNotFound('cannot open "%s"' % path)
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
    return packer_template


def add_local_image_tag(repository, template, tag):
    if 'post-processors' not in template:
        template['post-processors'] = []
    template['post-processors'].append([
        {
            'repository': repository,
            'tag': tag,
            'type': 'docker-import',
        }
    ])
    return template


def bootstrap_config(config, remove_publish=False, is_debug=False):
    command = ['packer', 'build']
    if is_debug:
        command.append('-debug')
    if remove_publish:
        image_repository = '{registry}/{name}'.format(**config)
        template = remove_publish_processes(config['packer'], PUBLISH_TYPES)
        template = add_local_image_tag(image_repository, template, DEFAULT_LOCAL_TAG)

        packer_template_path = write_config(template, PACKER_TMP_PATH)
        command.append(packer_template_path)
    else:
        command.append(config['packer'])
    return command


def cleanup_config():
    if os.path.exists(PACKER_TMP_PATH):
        shutil.rmtree(PACKER_TMP_ROOT)
