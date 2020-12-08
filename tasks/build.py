# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Build Task-Runner.'''

from invoke import task

from __version__ import __version__
# from . import config
from . import webapp
from . import webui
from . import docs


if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def start(ctx):
    '''Start all services.'''
    webapp.start(ctx)
    webui.start(ctx)
    docs.start(ctx)


@task
def stop(ctx):
    '''Stop all services.'''
    docs.stop(ctx)
    # webui.stop(ctx)
    webapp.stop(ctx)


@task
def version(
    ctx, part=part, tag=False, commit=False, message=None
):  # type: ignore
    '''Update project version and apply tags.'''
    args = [part]
    if tag:
        args.append('--tag')
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if message:
        args.append("--tag-message '{}'".format(message))
    ctx.run("bumpversion {}".format(' '.join(args)))


@task
def clean(ctx):  # type: ignore
    '''Clean project dependencies and build.'''
    paths = [
        '**/__pycache__',
        '**/*.pyc',
        '**/logs',
        '**/dist',
        '**/node_modules',
        '**/site',
        '**/flask_session',
    ]
    for path in paths:
        ctx.run("rm -rf {}".format(path))
