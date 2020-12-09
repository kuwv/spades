# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide play package.'''

# from sqlalchemy.dialects.postgresql import UUID

from spades import db
from spades.game.models.card import Card


class Play(db.Model):
    '''Represent player action.'''

    player_id = db.Column(
        db.Integer, db.ForeignKey('player.id'), primary_key=True
    )
    card_id = db.Column(
        db.Integer, db.ForeignKey('card.id'), primary_key=True
    )
    db.relationship(
        'Player', uselist=False, backref='plays', lazy='dynamic'
    )
    db.relationship(
        'Card', uselist=False, backref='plays', lazy='dynamic'
    )
    db.UniqueConstraint('player_id', 'card_id')

    def __init__(self, player_id: int, card_id: int):
        self.player_id = player_id
        self.card_id = card_id

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        card = Card.query.get(self.card_id)
        return (
            f"{self.__class__.__name__}(player={self.player_id!r}, card={card!r})"
        )
