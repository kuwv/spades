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
from spades.models.card import Card


def test_card() -> None:
    '''Test card object.'''
    card = Card('K', 'S')
    assert card.rank == 'K'
    assert card.suit == 'S'


def test_card_greater_spades() -> None:
    '''Test card value comparison.'''
    two_clubs = Card('2', 'C')
    ace_spades = Card('A', 'S')
    assert ace_spades > two_clubs


def test_card_greater_suit() -> None:
    '''Test card value comparison.'''
    ten_hearts = Card('T', 'H')
    jack_hearts = Card('J', 'H')
    assert jack_hearts > ten_hearts


def test_card_rank_error() -> None:
    '''Tst card rank error.'''
    with pytest.raises(InvalidRankCardException):
        Card('blah', 'H')


def test_card_suit_error() -> None:
    '''Test card suit error.'''
    with pytest.raises(InvalidSuitCardException):
        Card('T', 'blah')


def test_card_comparison_error() -> None:
    '''Test card comparison error.'''
    with pytest.raises(InvalidComparisonCardException):
        Card('T', 'H') > Card('T', 'C')
