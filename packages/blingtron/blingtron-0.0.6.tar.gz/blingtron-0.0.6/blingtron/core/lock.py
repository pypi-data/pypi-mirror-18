# -*- coding: utf-8 -*-
import os
import tarfile
import hashlib

LOCK_FILE = os.path.abspath('./.bling.lock')
TAR_FILE = os.path.abspath('./.lock.tar')


def md5sum_dir(dirname):
    if not os.path.isdir(dirname):
        raise TypeError('"%s" is not a directory' % dirname)

    with tarfile.open(TAR_FILE, 'w') as tar:
        tar.add(dirname, arcname=os.path.basename(dirname))

    hash_md5 = hashlib.md5()
    with open(TAR_FILE, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    try:
        os.remove(TAR_FILE)
    except OSError:
        pass
    return hash_md5.hexdigest()


def read_lock():
    try:
        with open(LOCK_FILE, 'rU') as f:
            return f.readline().strip('\n')
    except IOError:
        return None


def write_lock(dirname):
    with open(LOCK_FILE, 'w') as f:
        f.write(md5sum_dir(dirname))
