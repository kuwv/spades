# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide hand capabilities.'''

from typing import Optional, Set

from spades.card import Card
from spades.exceptions import MaxHandSizeException


class Hand:
    '''Provide player hand object.'''

    max_size = 13

    def __init__(self) -> None:
        '''Initialize player hand.'''
        self.__hand: Set[Card] = set()

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return (
            f"{self.__class__.__name__}(hand={self.__hand!r})"
        )

    def __iter__(self) -> 'Hand':
        '''Return hand itself as iterator.'''
        return self

    def __next__(self) -> Card:
        '''Get next card instance.'''
        if len(self.__hand) <= 0:
            raise StopIteration()
        return self.__hand

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        if len(self.__hand) < Hand.max_size:
            self.__hand.add(card)
        else:
            raise MaxHandSizeException('maximum hand size')

    def pull_card(self, rank: str, suit: str) -> Optional[Card]:
        selection = Card(rank, suit)
        for card in self.__hand:
            if selection == card:
                return card
        return None
