# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide play package.'''

from textwrap import dedent

# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.inspection import inspect

from spades import db
from spades.game.models.card import Card


class Play(db.Model):
    '''Represent player action.'''

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    player_id = db.Column(
        db.Integer, db.ForeignKey('player.id'), nullable=False
    )

    book = db.relationship(
        'Book', back_populates='plays'  # , lazy='dynamic'
    )
    card = db.relationship('Card')
    #     uselist=False, back_populates='plays', lazy='dynamic'
    # )
    player = db.relationship('Player')
    #     uselist=False, back_populates='plays', lazy='dynamic'
    # )
    db.UniqueConstraint('book_id', 'card_id', 'player_id')

    # def __init__(self, book_id: int, player_id: int, card_id: int) -> None:
    #     self.book_id = book_id
    #     self.player_id = player_id
    #     self.card_id = card_id

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        play = dedent(f"""\
            book_id={self.book_id!r},\
            player_id={self.player_id!r},\
            card={self.card!r}\
        """)
        return (
            f"{self.__class__.__name__}({play})"
        )

    @property
    def card(self) -> Card:
        return Card.query.get(self.card_id)
