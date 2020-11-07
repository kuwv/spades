# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide documentation task-runner.'''

import textwrap

from invoke import task


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
    with ctx.cd('docsite'):
        ctx.run('mkdocs build')


@task
def build(ctx):
    '''Build documentation site.'''
    with ctx.cd('docsite'):
        ctx.run('mkdocs build')


@task
def start(ctx, hostname='localhost', port=8081):  # type: ignore
    '''Start docsite.'''
    with ctx.cd('docsite'):
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
