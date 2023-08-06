# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import sys

# @see: http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
U_ERROR = '\033[1;31m✖ \033[0m'
U_WARNING = '\033[33m⚠ \033[0m'
U_INFO = '\033[34m➛ \033[0m'
U_OK = '\033[32m✓ \033[0m'


def err(message, exit_=True):
    print(U_ERROR + message, file=sys.stderr)
    if exit_:
        exit(1)


def warn(message):
    print(U_WARNING + message, file=sys.stderr)


def info(message, end='\n'):
    message = "{prefix} {message}".format(**{
        'prefix': U_INFO, 'message': message,
    })
    print(message, file=sys.stdout, end=end)


def ok(message):
    print(U_OK + message, file=sys.stdout)
