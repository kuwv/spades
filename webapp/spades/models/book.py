# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

from typing import List, Optional

from spades import config
from spades import exceptions
from spades.models.card import Card


class Book:
    '''Provide book object.'''

    def __init__(self) -> None:
        '''Initialize book.'''
        self.card_max = config.player_max
        self.__stack: List[Card] = []
        self.__trump: Optional[Card] = None
        self.__suit = None
        self.__lead_player = None

    def __repr__(self) -> str:
        '''Return string representation of book.'''
        return (
            f"{self.__class__.__name__}(stack={self.__stack!r})"
        )

    def __len__(self) -> int:
        '''Return length of book.'''
        return len(self.__stack)

    def __contains__(self, card: Card) -> bool:
        '''Check if book conatins card.'''
        return True if card in self.__stack else False

    @property
    def winner(self) -> Optional[None]:
        '''Get winner of book.'''
        return self.__lead_player

    @property
    def trump(self) -> Optional[Card]:
        '''Get current high card.'''
        return self.__trump

    @property
    def suit(self) -> Optional[str]:
        '''Get opening suit of book.'''
        return self.__suit

    def add_trick(self, player_id: int, card: Card) -> None:
        '''Add card to book.'''
        # print('trick', player_id, card)
        if len(self.__stack) < self.card_max:
            if self.__stack == []:
                self.__lead_player = player_id
                self.__suit = card.suit
                self.__trump = card
            elif self.__suit == card.suit or card.suit == 'S':
                if self.__trump < card:
                    self.__lead_player = player_id
                    self.__trump = card
            self.__stack.append(card)
        else:
            raise exceptions.MaxBookSizeException('max book size')
