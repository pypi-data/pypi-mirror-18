# -*- coding: utf-8 -*-
from .git import get_current_branch
from .git import get_current_commit

from ..domain.vendor import GitError

# @see: https://docs.travis-ci.com/user/environment-variables/
#
# Below are the list of TravisCI environment variables we use in our builds.
REQUIRED_TRAVIS_ENV = {
    'TRAVIS_BRANCH': get_current_branch,
    'TRAVIS_COMMIT': get_current_commit,
}


def patch_environ(environ):
    environ = environ.copy()
    for env in REQUIRED_TRAVIS_ENV:
        if environ.get(env) is not None:
            continue
        try:
            environ[env] = REQUIRED_TRAVIS_ENV[env]()
        except GitError:
            environ[env] = None
    return environ
