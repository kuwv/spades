# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Build Task-Runner.'''

from invoke import task

from __version__ import __version__
# from . import config
from . import config
from . import compose
from . import pki


@task
def setup(ctx):
    pki.setup(ctx)


@task
def start(ctx):
    '''Start all services.'''
    compose.start(ctx)


@task
def stop(ctx):
    '''Stop all services.'''
    compose.stop(ctx)
