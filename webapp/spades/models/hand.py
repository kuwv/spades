# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide hand capabilities.'''

import json
from typing import List

# from flask import session

from spades import exceptions
from spades.models.card import Card, CardEncoder


class Hand:
    '''Provide player hand object.'''

    spades_broken = False
    max_size = 13

    def __init__(self) -> None:
        '''Initialize player hand.'''
        self.__hand: List[Card] = []

    def __repr__(self) -> str:
        '''Return string representation of card.'''
        return f"{self.__class__.__name__}(hand={self.__hand!r})"

    def __len__(self) -> int:
        '''Return number of items.'''
        return len(self.__hand)

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

    @property
    def to_json(self):
        '''Get json instance.'''
        return(json.dumps(self.__hand, cls=CardEncoder))

    def list_suit(self, suit: str) -> List[str]:
        '''List items of a suit.'''
        return [c.rank for c in self.__hand if c.suit == suit]

    def get_suit(self, suit: str) -> List[Card]:
        '''Get all items of a suit.'''
        return [c for c in self.__hand if c.suit == suit]

    def playable(self, suit: str = None) -> List[Card]:
        '''Get all playable cards.'''
        if not suit and not Hand.spades_broken:
            hand = [c for c in self.__hand if c.suit != 'S']
            return self.__hand if hand == [] else hand
        elif suit and len(self.get_suit(suit)) > 0:
            return self.get_suit(suit)
        else:
            return self.__hand

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        if len(self.__hand) < Hand.max_size:
            if card not in self.__hand:
                self.__hand.append(card)
            else:
                exceptions.InvalidDeckException(
                    'duplicate card already in hand'
                )
        else:
            raise exceptions.MaxHandSizeException('maximum hand size')

    def pull_card(self, rank: str, suit: str) -> Card:
        '''Pull card from hand to play.'''
        selection = Card(rank, suit)
        for card in self.__hand:
            if selection == card:
                if selection.suit == 'S':
                    Hand.spades_broken = True
                self.__hand.remove(card)
                return card
        raise exceptions.IllegalPlayException('player does not hold card')
