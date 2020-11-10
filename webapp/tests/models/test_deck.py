# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for deck.'''

from spades.card import Card
from spades.deck import Deck


def test_deck():
    '''Test deck.'''
    deck = Deck()
    cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
    for card in deck:
        assert card in cards