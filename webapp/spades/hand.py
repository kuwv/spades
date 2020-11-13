# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide hand capabilities.'''

from typing import Optional, List

from spades.card import Card
from spades.exceptions import MaxHandSizeException


class Hand:
    '''Provide player hand object.'''

    max_size = 13

    def __init__(self) -> None:
        '''Initialize player hand.'''
        self.__hand: List[Card] = []

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return (
            f"{self.__class__.__name__}(hand={self.__hand!r})"
        )

    def __iter__(self) -> 'Hand':
        '''Return hand itself as iterator.'''
        self.__count = 0
        return self

    def __next__(self) -> Card:
        '''Get next card instance.'''
        if self.__count >= len(self.__hand):
            raise StopIteration()
        card: Card = self.__hand[self.__count]
        self.__count += 1
        return card

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        if len(self.__hand) < Hand.max_size:
            self.__hand.append(card)
        else:
            raise MaxHandSizeException('maximum hand size')

    def pull_card(self, rank: str, suit: str) -> Optional[Card]:
        selection = Card(rank, suit)
        for card in self.__hand:
            if selection == card:
                return card
        return None
