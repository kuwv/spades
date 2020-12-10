# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Initialize project management tasks.'''

from invoke import Collection

from . import (
    compose, docs, webui, webapp, build, pki, qa, setup, validate
)

ns = Collection().from_module(setup)
ns.add_collection(Collection.from_module(build))
ns.add_collection(Collection.from_module(compose))
ns.add_collection(Collection.from_module(pki))
ns.add_collection(Collection.from_module(webapp))
ns.add_collection(Collection.from_module(webui))
ns.add_collection(Collection.from_module(docs))
ns.add_collection(Collection.from_module(qa))
ns.add_collection(Collection.from_module(validate))
