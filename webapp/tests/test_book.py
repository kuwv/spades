# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test book.'''

import pytest

from spades.exceptions import MaxBookSizeException
from spades.card import Card
from spades.book import Book


def test_book():
    '''Test card in book.'''
    book = Book()
    book.add_card(Card('K', 'Spades'))
    assert Card('K', 'Spades') in book


def test_book_trump():
    '''Test high card in book.'''
    book = Book()
    book.add_card(Card('2', 'Diamonds'))
    book.add_card(Card('10', 'Diamonds'))
    assert book.trump == Card('10', 'Diamonds')


def test_book_max():
    '''Test maximum allowed cards in book.'''
    book = Book(1)
    with pytest.raises(MaxBookSizeException):
        book.add_card(Card('2', 'Hearts'))
        book.add_card(Card('3', 'Hearts'))
