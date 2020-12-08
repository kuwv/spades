# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

# from uuid import uuid4

from flask_login import UserMixin
from passlib.hash import argon2
# from sqlalchemy.dialects.postgresql import UUID

# from spades import exceptions
from spades import db


class User(UserMixin, db.Model):
    '''Provide user object.'''

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return (
            f"{self.__class__.__name__}(username={self.username!r})"
        )

    def set_password(self, password: str) -> None:
        '''Set user password.'''
        self.password = argon2.hash(password)

    def check_password(self, password: str) -> bool:
        '''Check user password.'''
        return argon2.verify(password, self.password)

    def add_win(self) -> None:
        self.wins += 1

    def add_loss(self) -> None:
        self.losses += 1
