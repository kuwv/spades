# -*- coding: utf-8 -*-
# type: ignore
'''Provide player hand tests.'''

from spades import db
from spades.game.models.card import Card
from spades.game.models.player import Hand


def test_hand(app) -> None:
    '''Test hand.'''
    hand = Hand()
    hand.add_card(Card('A', 'S'))
    db.session.add(hand)
    db.session.commit()

    card = hand.pull_card('A', 'S')
    assert card.rank == 'A'
    assert card.suit == 'S'
