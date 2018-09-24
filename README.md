# Ssanic - simple web server for TP HighLoad course

[![Build Status](https://travis-ci.org/jpyatachkov/ssanic.svg?branch=master)](https://travis-ci.org/jpyatachkov/ssanic)

![sanic](https://proxy.duckduckgo.com/iur/?f=1&image_host=http%3A%2F%2Ffc08.deviantart.net%2Ffs70%2Ff%2F2011%2F216%2F3%2Fa%2Fi_drew_sanic_hegehog_by_andyparka-d44xhhu.jpg&u=http://orig08.deviantart.net/402f/f/2011/216/3/a/i_drew_sanic_hegehog_by_andyparka-d44xhhu.jpg)

`asyncio`-based dummy implementation of simple web server.
Some kind of travesty on [sanic project](https://github.com/huge-success/sanic), but the name of this repo speaks to itself.

This task is done due to [HighLoad course 1st homework](https://github.com/init/http-test-suite).

## How to run

There are several ways to do it.

### From Docker

**Before build** Provide directory with static files and config file (by default `httpd.conf`
from this repo is used).

**Notice** That to work correct in Docker host **MUST** be `0.0.0.0` and port **MUST** be `80`!

Example command suite:

```text
docker build -t ssanic https://github.com/jpyatachkov/ssanic.git
docker run -p 80:80 -v ~/documents:/var/www/documents:ro -v ~/httpd.conf:/etc/httpd.conf:ro --name ssanic ssanic
```

### From git as python package

```text
pip install git+https://github.com/jpyatachkov/ssanic.git
```

After executing this command you will be able to run `ssanic` from
current python interpreter. This command is alias for `ssanic.__main__`, so see next
section for CLI arguments interface details.

### From source

`ssanic.__main__` is main file of Ssanic - it handles master process,
reads configuration and forks Ssanic worker processes. It has particular CLI interface:

```text
usage: __main__.py [-h] [--document_root DOCUMENT_ROOT] [--host HOST]
                   [--port PORT] [--num-workers NUM_WORKERS]
                   [--config-file CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --document_root DOCUMENT_ROOT
                        directory to serve static files from
  --host HOST           host to bind to
  --port PORT           port to listen to
  --num-workers NUM_WORKERS
                        number of workers
  --config-file CONFIG_FILE
                        path to config file (if provided, all other CLI args will be
                        ignored - their values would be obtained from config file)
```

`ssanic.worker` is single worker. If you don't want to deal with several workers,
just run this file. It does not have any CLI interface, so you are to configure it
(just `host`, `port` and `document_root`) through source code.
