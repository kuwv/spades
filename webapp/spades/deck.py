# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide card package.'''

import random

from .card import Card


class Deck:
    '''Provide deck object.'''

    size = 52

    def __init__(self):
        self.deck = [
            Card(rank, suit) for rank in Card.ranks for suit in Card.suits
        ]
        self.shuffle()

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.deck) <= 0:
            raise StopIteration()

        return self.deck.pop()

    def shuffle(self, iterations=50):
        random.shuffle(self.deck)
