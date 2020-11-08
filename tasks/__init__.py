# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Initialize project management tasks.'''

from invoke import Collection

from . import docs, webui, webapp, build, qa, validate

ns = Collection().from_module(build)
ns.add_collection(Collection.from_module(webapp))
ns.add_collection(Collection.from_module(webui))
ns.add_collection(Collection.from_module(docs))
ns.add_collection(Collection.from_module(qa))
ns.add_collection(Collection.from_module(validate))
