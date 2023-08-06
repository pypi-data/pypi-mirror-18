# -*- coding: utf-8 -*-
import os
import json
import shutil

from ..core.lock import md5sum_dir
from ..core.lock import read_lock
from ..domain.vendor import PackerConfigNotFound
from ..config import config as app_conf


def is_packer_updated(packer_dir):
    old_hash = read_lock()
    new_hash = md5sum_dir(packer_dir)
    return old_hash and old_hash != new_hash


def read_config(path, packer_config_file=app_conf.packer.config_file):
    path = os.path.join(path, packer_config_file)
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


def replace_post_processor(packer_path, name, tag):
    packer_template = read_config(packer_path)
    packer_template = packer_template.copy()
    packer_template['post-processors'] = []
    packer_template['post-processors'].append([
        {
            'repository': name,
            'tag': tag,
            'type': 'docker-import',
        }
    ])
    return packer_template


def bootstrap_config(
        config, should_publish, is_debug,
        default_local_tag=app_conf.docker.default_local_tag,
        packer_tmp_path=app_conf.packer.tmp_path,
        packer_config_file=app_conf.packer.config_file):
    """Update the Packer config file depending on how we want to produce an image."""

    command = ['packer', 'build']
    if is_debug:
        command.append('-debug')
    if should_publish:
        command.append(os.path.join(config.get('packer'), packer_config_file))
    else:
        template = replace_post_processor(
            config.get('packer'),
            config.get('image_name'),
            default_local_tag
        )
        packer_template_path = write_config(template, packer_tmp_path)
        command.append(packer_template_path)
    return command


def cleanup_config(packer_tmp_root=app_conf.packer.tmp_root, packer_tmp_path=app_conf.packer.tmp_path):
    """Removes the temporary packer dumping ground directory if exists."""
    if os.path.exists(packer_tmp_path):
        shutil.rmtree(packer_tmp_root)
