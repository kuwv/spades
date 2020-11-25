# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Configurations for Task-Runners.'''

import os
import platform

# System setup
if platform.system() == 'Windows':
    __bin_subpath = os.path.join('bin')

if platform.system() == 'Darwin':
    __bin_subpath = os.path.join('Library', 'bin')

if platform.system() == 'Linux':
    __bin_subpath = os.path.join('.local', 'bin')

system_type = platform.system().lower()

# Versions
mkcert_version = os.getenv('MKCERT_VERSION', 'v1.4.2')

# Paths
project_path = os.getenv('PROJECT_PATH', '.')
bin_path = os.path.join(os.path.expanduser('~'), __bin_subpath)
static_dir = 'static'
webui_dir = os.path.join(static_dir, 'webui')
docs_dir = static_dir
webapp_dir = 'webapp'

# Settings
environment = os.getenv('FLASK_ENV', 'development')
