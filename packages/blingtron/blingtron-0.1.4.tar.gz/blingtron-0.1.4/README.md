# Blingtron

[![Build Status](https://travis-ci.org/ImageIntelligence/blingtron.svg?branch=master)](https://travis-ci.org/ImageIntelligence/blingtron)
[![PyPI version](https://badge.fury.io/py/blingtron.svg)](https://badge.fury.io/py/blingtron)

**Welcome to Blingtron!**

> Assembles the upgraded [Blingtron 5000](http://www.wowhead.com/item=111821/blingtron-5000), a savage, yet generous, robot. While he will give out gifts to players once per day, he will also fight other Blingtron units to the death. (4 Hrs Cooldown)

Blingtron is a simple command line too (CLI) aimed at helping developers run their Image Intelligence projects.

## Installation

```
$ pip install blingtron
```

Projects that use Blingtron are expected to have a `bling.json` file at the root of the project directory structure. For an example of what a bling.json file might look like, checkout [bling.example.json](./bling.example.json).

* `name`: The name of your project
* `registry`: The username of your account for your image registry
* `run`: The command that's executed when a Docker container runs your image (remotely)
* `start`: The arguments passed into `docker run`(locally)
* `packer`: The location of your Packer configuration directory
* `env`: An object of custom environ variables you can pass into all `bling` commands

See [imageintelligence/skeleton-python](https://github.com/ImageIntelligence/skeleton-python) and [imageintelligence/skeleton-scala](https://github.com/ImageIntelligence/skeleton-scala) for more examples.

## Usage

```
>>> bling --help
bling.py

usage:
    bling start
    bling stop
    bling run
    bling build [--publish] [--debug]

commands:
    start         starts app inside an interactive container
    stop          stops running container
    run           starts app inside a container, executing the specified run command
    build         invokes `packer build` with packer template json file

options:
    --publish     publishes the build artifact to a remote registry
    --debug       enables debug mode

    -h --help     shows this
    -v --version  shows version
```

Example workflow:

```
$ bling build
$ bling start
```

## Development

Clone the project:

```
$ git clone git@github.com:ImageIntelligence/blingtron.git
```

Setup your virtualenv:

```
$ mkvirtualenv blingtron
```

Attach `bling` to your shell:

```
$ python setup.py develop
```

## Deployment

Create a `~/.pypirc` and replace the username and password with real credentials:

```
[distutils]
index-servers =
  blingtron

[blingtron]
repository=https://pypi.python.org/pypi
username=xxx
password=yyy
```

Register this package to the Cheeseshop:

```
$ python setup.py register -r blingtron
```

Build a distributable and upload:

```
$ python setup.py sdist upload -r blingtron
```
