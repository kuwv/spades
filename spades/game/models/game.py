# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide game model package.'''

# from uuid import uuid4
# from sqlalchemy.dialects.postgresql import UUID

from spades import db  # , exceptions


class Game(db.Model):
    '''Provide game object.'''

    id = db.Column(db.Integer, primary_key=True)
    # players = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # matches = db.Column(UUID(as_uuid=True))
