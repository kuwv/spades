# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for deck.'''

from spades import db
from spades.game.models.card import Card
from spades.game.models.deck import Deck


def test_deck(app):
    '''Test deck.'''
    deck = Deck()
    db.session.add(deck)
    db.session.commit()

    cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
    for card in cards:
        assert card in deck.cards

    for card in deck:
        assert card not in deck.cards

    db.session.delete(deck)
    db.session.commit()
