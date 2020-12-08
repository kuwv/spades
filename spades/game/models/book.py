# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

from typing import List, Optional
# from uuid import uuid4

# from sqlalchemy.dialects.postgresql import UUID

from spades import config, db, exceptions
from spades.game.models.card import Card


class Book(db.Model):
    '''Provide book object.'''

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # stack = db.relationship('Card', uselist=True, backref='Book')
    trump = db.Column(db.Boolean, unique=False, default=False)
    suit = db.Column(db.String(1), unique=False)
    lead_player = db.Column(db.Integer, db.ForeignKey('user.id'))
    # player =

    def __init__(self) -> None:
        '''Initialize book.'''
        self.card_max = config.player_max
        self.stack: List[Card] = []
        # self.trump: Optional[Card] = None
        self.suit = None
        # self.lead_player = None

    def __repr__(self) -> str:
        '''Return string representation of book.'''
        return (
            f"{self.__class__.__name__}(stack={self.__stack!r})"
        )

    def __len__(self) -> int:
        '''Return length of book.'''
        return len(self.stack)

    def __contains__(self, card: Card) -> bool:
        '''Check if book conatins card.'''
        return True if card in self.stack else False

    @property
    def winner(self) -> Optional[None]:
        '''Get winner of book.'''
        # TODO: refactor to get winner from stack
        return self.lead_player

    # @property
    # def trump(self) -> Optional[Card]:
    #     '''Get current high card.'''
    #     return self.__trump

    # @property
    # def suit(self) -> Optional[str]:
    #     '''Get opening suit of book.'''
    #     return self.__suit

    def add_trick(self, player_id: int, card: Card) -> None:
        '''Add card to book.'''
        # print('trick', player_id, card)
        if len(self.stack) < self.card_max:
            if self.stack == []:
                self.lead_player = player_id
                self.suit = card.suit
                self.trump = card
            elif self.suit == card.suit or card.suit == 'S':
                if self.trump < card:
                    self.lead_player = player_id
                    self.trump = card
            self.stack.append(card)
        else:
            raise exceptions.MaxBookSizeException('max book size')
