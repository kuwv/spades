# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide card package.'''

import json

from spades.exceptions import (
    InvalidComparisonCardException,
    InvalidRankCardException,
    InvalidSuitCardException
)


class CardEncoder(json.JSONEncoder):
    '''Encode cards into JSON.'''

    def default(self, o):
        '''Provide default card encoder implementation.'''
        return {'rank': o.rank, 'suit': o.suit}


class Card:
    '''Provide card object.'''

    ranks: tuple = (
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
    )
    suits: tuple = ('C', 'D', 'H', 'S')

    def __init__(self, rank: str, suit: str) -> None:
        '''Initialize card.'''
        if rank in Card.ranks:
            self.rank = rank
        else:
            raise InvalidRankCardException('except on incorrect rank')

        if suit.lower().capitalize() in Card.suits:
            self.suit = suit.lower().capitalize()
        else:
            raise InvalidSuitCardException('except on incorrect suit')

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return (
            f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r})"
        )

    def __hash__(self) -> int:
        '''Check object hash.'''
        return hash((self.rank, self.suit))

    def __eq__(self, other: object) -> bool:
        '''Check if card is equal another card.'''
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (
            (self.rank, self.suit) == (other.rank, other.suit)  # type: ignore
        )

    def __gt__(self, other: 'Card') -> bool:
        '''Check if card is greater than other.'''
        if not other:
            return True
        if self.suit == other.suit:
            return Card.ranks.index(self.rank) > Card.ranks.index(other.rank)
        elif self.suit == 'S':
            return True
        elif other.suit == 'S':
            return False
        else:
            raise InvalidComparisonCardException(
                'except for invalid comparison'
            )
            # return Card.suits.index(self.suit) > Card.suits.index(other.suit)
