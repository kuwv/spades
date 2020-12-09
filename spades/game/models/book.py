# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

from typing import Optional
# from uuid import uuid4

# from sqlalchemy.dialects.postgresql import UUID

from spades import config, db, exceptions
from spades.game.models.card import Card
from spades.game.models.play import Play

plays = db.Table(
    'book_of_plays',
    db.Column(
        'book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True
    ),
    db.Column('player_id', db.Integer, primary_key=True),
    db.Column('card_id', db.Integer, primary_key=True),
    db.ForeignKeyConstraint(
        ['player_id', 'card_id'], ['play.player_id', 'play.card_id']
    )
)


class Book(db.Model):
    '''Provide book object.'''

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # TODO stack should link current book to game
    # stack = db.relationship('GameState', uselist=False, backref='Book')
    plays = db.relationship(
        'Play',
        secondary=plays,
        lazy='subquery',
        backref=db.backref('book_of_plays', lazy=True)
    )

    def __init__(self) -> None:
        '''Initialize book.'''
        self.card_max = config.player_max
        self.lead_player = None

    def __repr__(self) -> str:
        '''Return string representation of book.'''
        return (
            f"{self.__class__.__name__}(book={self.plays!r})"
        )

    def __len__(self) -> int:
        '''Return length of book.'''
        return len(self.plays)

    def __contains__(self, card: Card) -> bool:
        '''Check if book conatins card.'''
        # TODO: need lookup here
        return True if card in self.plays else False

    @property
    def winner(self) -> Optional[str]:
        '''Get winner of book.'''
        # TODO: refactor to get winner from stack
        if not self.trump:
            return None
        else:
            return self.trump
        return self.lead_player

    # TODO: check if trump has ben played

    @property
    def trump(self) -> Optional[Card]:
        '''Get current high card.'''
        # TODO: rename highcard
        if self.plays == []:
            return None
        trump = None
        for card in self.plays:
            if not trump:
                trump = card
            elif card > trump:
                trump = card
        return trump

    @property
    def suit(self) -> Optional[str]:
        '''Get opening suit of book.'''
        if self.plays == []:
            return None
        return self.plays[0].suit

    def add_trick(self, play: Play) -> None:
        '''Add card to book.'''
        # print('trick', player_id, card)
        if len(self.plays) < self.card_max:
            self.plays.append(play)
        else:
            raise exceptions.MaxBookSizeException('max book size')
