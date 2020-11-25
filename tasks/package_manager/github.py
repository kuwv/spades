# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Validation Task-Runner.'''

import os

from invoke import task

from .. import config
from .. import filesystem


@task
def install(
    ctx,
    repo,
    version,
    filename=None,
    new_filename=None,
    file_pattern=f"*{config.system_type}*"
):
    '''Install GitHub release.'''
    try:
        filesystem.mkdir(ctx, config.bin_path)
        with ctx.cd(config.bin_path):
            ctx.run(f"github-asset {repo} download {version} '{file_pattern}'")
            if filename:
                __filepath = os.path.join(config.bin_path, filename)
                if new_filename:
                    if os.path.exists(__filepath):
                        __new_filepath = os.path.join(
                            config.bin_path, new_filename
                        )
                        if not os.path.exists(__new_filepath):
                            os.rename(__filepath, __new_filepath)
                            __filepath = __new_filepath
                if os.name == 'posix':
                    st = os.stat(__filepath)
                    os.chmod(__filepath, st.st_mode | 0o111)
    except OSError as err:
        print(f"unable to download github release due to: {err}")
