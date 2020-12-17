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


class Book(db.Model):
    '''Provide book object.'''

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # TODO stack should link current book to game
    # stack = db.relationship('GameState', uselist=False, backref='Book')
    plays = db.relationship(
        'Play',
        uselist=True,
        lazy='subquery',
        backref='Book',
    )

    def __init__(self) -> None:
        '''Initialize book.'''
        self.card_max = config.player_max

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
    def winning_play(self) -> Optional[Card]:
        '''Get current high card.'''
        # TODO: rename highcard
        if self.plays == []:
            return None
        high_play = None
        for play in self.plays:
            if not high_play or play.card > high_play.card:
                high_play = play
        return high_play

    @property
    def winner(self) -> Optional[str]:
        '''Get winner of book.'''
        # TODO: refactor to get winner from stack
        if self.plays == []:
            return None
        else:
            return self.winning_play

    @property
    def broken(self) -> bool:
        for play in self.plays:
            if play.card.suit == 'S':
                return True
        return False

    @property
    def high_card(self) -> Optional[Card]:
        '''Get current high card.'''
        # TODO: rename highcard
        if self.plays == []:
            return None
        else:
            return self.winning_play.card

    @property
    def suit(self) -> Optional[str]:
        '''Get opening suit of book.'''
        if self.plays == []:
            return None
        return self.plays[0].card.suit

    def add_play(self, play: Play) -> None:
        '''Add card to book.'''
        # print('trick', player_id, card)
        if len(self.plays) < self.card_max:
            self.plays.append(play)
        else:
            raise exceptions.MaxBookSizeException('max book size')
