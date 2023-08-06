# -*- coding: utf-8 -*-
import os
import subprocess

LOCK_FILE = os.path.abspath('./.bling.lock')


def md5sum_dir(dirname):
    if not os.path.isdir(dirname):
        raise TypeError('"%s" is not a directory' % dirname)
    p = subprocess.Popen(['tar', '-cf', '-', dirname], stdout=subprocess.PIPE)
    p = subprocess.Popen('md5sum', stdin=p.stdout, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.split(' ')[0]


def read_lock():
    try:
        with open(LOCK_FILE, 'rU') as f:
            return f.readline().strip('\n')
    except IOError:
        return None


def write_lock(dirname):
    with open(LOCK_FILE, 'w') as f:
        f.write(md5sum_dir(dirname))
