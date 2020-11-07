# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Build Task-Runner.'''

from invoke import task

from webapp.__version__ import __version__

if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def build(ctx, path='.'):  # type: ignore
    '''Build docker image.'''
    ctx.run(f"docker build {path}")


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
    ]
    for path in paths:
        ctx.run("rm -rf {}".format(path))
