# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for card.'''

import pytest

from spades.exceptions import (
    InvalidRankCardException,
    InvalidSuitCardException,
    InvalidComparisonCardException
)
from spades.card import Card


def test_card():
    '''Test card object.'''
    card = Card('K', 'Spades')
    assert card.rank == 'K'
    assert card.suit == 'Spades'


def test_card_greater_spades():
    '''Test card value comparison.'''
    two_clubs = Card('2', 'Clubs')
    ace_spades = Card('A', 'Spades')
    assert ace_spades > two_clubs


def test_card_greater_suit():
    '''Test card value comparison.'''
    ten_hearts = Card('10', 'Hearts')
    jack_hearts = Card('J', 'Hearts')
    assert jack_hearts > ten_hearts


def test_card_rank_error():
    '''Tst card rank error.'''
    with pytest.raises(InvalidRankCardException):
        Card('blah', 'Hearts')


def test_card_suit_error():
    '''Test card suit error.'''
    with pytest.raises(InvalidSuitCardException):
        Card('10', 'blah')


def test_card_comparison_error():
    '''Test card comparison error.'''
    with pytest.raises(InvalidComparisonCardException):
        Card('10', 'Hearts') > Card('10', 'Clubs')
