# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide documentation task-runner.'''

import textwrap

from invoke import task

from . import config


@task
def lint(ctx):
    '''Check code for documentation errors.'''
    ctx.run('pydocstyle')


@task
def coverage(ctx):
    '''Ensure all code is documented.'''
    ctx.run('docstr-coverage **/*.py')


@task(pre=[lint], post=[coverage])
def test(ctx):
    '''Test documentation build.'''
    with ctx.cd(config.docs_dir):
        ctx.run('mkdocs build')


@task
def build(ctx):
    '''Build documentation site.'''
    with ctx.cd(config.docs_dir):
        ctx.run('mkdocs build')


@task
def start(ctx, hostname='localhost', port=8001):  # type: ignore
    '''Start docsite.'''
    with ctx.cd(config.docs_dir):
        ctx.run(
            textwrap.dedent(f"""\
                mkdocs serve \
                --dev-addr={hostname}:{port} \
                --livereload
            """),
            disown=True,
        )


@task
def stop(ctx):  # type: ignore
    '''Stop docsite.'''
    ctx.run('pkill mkdocs')
