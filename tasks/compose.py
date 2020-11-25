# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Build Task-Runner.'''

from invoke import task

from . import config


@task
def start(ctx, build=False, recreate=False):
    '''Start all compose containers.'''
    args = []
    if build:
        args.append('--build')
    if recreate:
        args.append('--force-recreate')
    with ctx.cd(config.project_path):
        ctx.run("docker-compose up -d {a}".format(a=' '.join(args)))


@task
def stop(ctx, remove_images=None, remove_volumes=True, remove_orphans=True):
    '''Stop all compose containers.'''
    args = []
    if remove_images:
        args.append(f"--rmi={remove_images}")
    if remove_volumes:
        args.append('--volumes')
    if remove_orphans:
        args.append('--remove-orphans')
    with ctx.cd(config.project_path):
        ctx.run("docker-compose down {a}".format(a=' '.join(args)))
