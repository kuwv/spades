# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide card package.'''

from random import randrange, shuffle

from spades.game.models.card import Card


class Deck:
    '''Provide deck object.'''

    max_size = 52

    def __init__(self) -> None:
        '''Initialize Deck.'''
        self.__deck = [
            Card(rank, suit) for rank in Card.ranks for suit in Card.suits
        ]
        self.shuffle()

    def __iter__(self) -> 'Deck':
        '''Return deck itself as iterator.'''
        return self

    def __next__(self) -> Card:
        '''Get next card instance.'''
        if len(self.__deck) <= 0:
            raise StopIteration()
        return self.__deck.pop()

    def shuffle(self, cycles: int = 99) -> None:
        '''Mimic dealer shuffling.'''
        for _ in range(randrange(cycles)):
            shuffle(self.__deck)
