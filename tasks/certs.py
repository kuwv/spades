# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Validation Task-Runner.'''

import platform

from invoke import task

from . import config
from . import filesystem
from .package_manager import github

mkcert = f"mkcert-{config.mkcert_version}-{config.system_type}-amd64"


@task
def setup(ctx):
    '''Install GitHub release.'''
    github.install(
        ctx,
        repo='FiloSottile/mkcert',
        version=config.mkcert_version,
        filename=mkcert,
        new_filename='mkcert',
        file_pattern=f"*{platform.system().lower()}-amd64*"
    )
    ctx.run('mkcert -install')


@task(pre=[setup], iterable=['name'])
def gencert(
    ctx,
    name,
    key=None,
    cert=None,
    p12=None,
    client=None,
    csr=None,
    ecdsa=False,
    pkcs12=False,
    path=None,
):
    '''Generate certificate.'''
    args = []
    if key:
        args.append(f"-key-file={key}")
    if cert:
        args.append(f"-cert-file={cert}")
    if p12:
        args.append(f"-client={client}")
    if ecdsa:
        args.append(f"-ecdsa={ecdsa}")
    if pkcs12:
        args.append(f"-pkcs12={pkcs12}")
    if csr:
        args.append(f"-csr={csr}")
    cmd = "mkcert {a} {n}".format(a=' '.join(args), n=' '.join(name))
    if path:
        filesystem.mkdir(ctx, path)
        with ctx.cd(path):
            ctx.run(cmd)
    else:
        ctx.run(cmd)


@task
def cleanup(ctx, path=None):
    '''Cleanup certificates.'''
    if path:
        filesystem.rmdir(ctx, path)
    ctx.run('mkcert -uninstall')
