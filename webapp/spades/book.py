# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide book package.'''

from typing import List

from .card import Card


class Book:
    '''Provide book object.'''

    def __init__(self, max_size: int = 4):
        '''Initialize book.'''
        self.__max_size
        self.__cards: List[Card] = []

    def __repr__(self):
        '''Return string representation of book.'''
        return (
            f"{self.__class__.__name__}(cards={self.__cards!r})"
        )

    def __len__(self):
        '''Return length of book.'''
        return len(self.__cards)

    def __contains__(self, card: Card):
        '''Check if book conatins card.'''
        return True if card in self.__cards else False

    def add_card(self, card: Card):
        '''Add card to book.'''
        if len(self.__cards) < self.__max_size:
            self.__cards.append(card)
        else:
            print('except on boox at max size')
