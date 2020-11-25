# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide App Task-Runner.'''

import os
import textwrap

from invoke import task

from . import config


def build(ctx, path='.'):  # type: ignore
    '''Build docker image.'''
    ctx.run(f"""\
        pipenv lock \
        --requirements > {config.webapp_dir}/requirements.txt
    """)
    with ctx.cd(config.webapp_dir):
        ctx.run(f"docker build {path}")


@task
def start(ctx, hostname='localhost', port=8080, workers=4):  # type: ignore
    '''Start webapp.'''
    with ctx.cd(config.webapp_dir):
        ctx.run(
            textwrap.dedent(f"""\
                gunicorn app:app \
                --pid={os.getcwd()}/.pid \
                --bind={hostname}:{port} \
                --workers={workers} \
                --reload
            """),
            disown=True,
        )


@task
def stop(ctx):  # type: ignore
    '''Stop webapp.'''
    ctx.run('pkill gunicorn')
