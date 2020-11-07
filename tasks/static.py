# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Static Content Task-Runner.'''

from invoke import task


@task
def install(ctx, path='static', also='dev'):
    with ctx.cd(path):
        ctx.run(f"npm install --also={also}")


@task(pre=[install])
def build(ctx, path='static'):
    '''Build static content.'''
    with ctx.cd(path):
        ctx.run('npm run build')
