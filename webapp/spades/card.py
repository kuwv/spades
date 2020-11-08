# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide card capabilities.'''


class Card:
    '''Provide card object.'''

    ranks: tuple = (
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
    )
    suits: set = {'Clubs', 'Diamonds', 'Hearts', 'Spades'}

    def __init__(self, rank: str, suit: str):
        '''Initialize card.'''
        if rank in Card.ranks:
            self.rank = rank
        else:
            print('except on incorrect rank')

        if suit in Card.suits:
            self.suit = suit
        else:
            print('except on incorrect suit')

    def __repr__(self):
        '''Return string representation of card.'''
        return (
            f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r})"
        )

    def __eq__(self, other):
        '''Check if card is equal another card.'''
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)
