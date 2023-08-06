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

Projects that use Blingtron are expected to have a `.bling.json` file at the root of the project directory structure. For example:

```json
{
  "name": "scala-project",
  "image": "imageintelligence/scala",
  "run": "sbt run",
  "start": [
    "-v ./:/app",
    "-v ~/.ivy2:/root/.ivy2",
    "-v ~/.sbt:/root/.sbt",
    "-p 127.0.0.1:8080:8080",
    "-i -t",
    "--rm",
    "--workdir /app",
    "--name", "$NAME",
    "$IMAGE", "/bin/bash"
  ]
}
```

* `name`: The name of your project
* `run`: The command that's executed when a Docker container runs your image
* `start`: Runs your image locally and within bash

See [imageintelligence/skeleton-python](https://github.com/ImageIntelligence/skeleton-python) and [imageintelligence/skeleton-scala](https://github.com/ImageIntelligence/skeleton-scala) for more examples.

## Usage

```
$ bling --help
```

**Note:** Invoking `bling` without any arguments will execute `start` with the default arguments.

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
