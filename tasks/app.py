# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test Task-Runner.'''

import os
import textwrap
from invoke import task


@task
def start(
    ctx,
    hostname='localhost',
    port=9000,
    workers=4
):  # type: ignore
    '''Start webapp.'''
    ctx.run(
        textwrap.dedent(f"""\
            gunicorn app:app \
            --pid {os.getcwd()}/.pid \
            --workers={workers} \
            --reload
        """),
        disown=True
    )


@task
def stop(ctx):  # type: ignore
    '''Stop webapp.'''
    ctx.run('pkill gunicorn')
