# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

from typing import Optional, Set

from spades import exceptions
from spades.book import Book
from spades.card import Card
from spades.hand import Hand


class User:
    '''Provide user object.'''

    def __init__(self, name: str) -> None:
        '''Initialize user.'''
        self.__name = name

    @property
    def name(self) -> str:
        '''Get user name.'''
        return self.__name


class Player(User):
    '''Provide player object.'''

    def __init__(self, name: str) -> None:
        '''Initialize player.'''
        super().__init__(name)
        self.__hand: Optional[Hand] = None
        self.__books: Set[Book] = set()
        self.__bid: Optional[int] = None

    @property
    def hand(self) -> Optional[Hand]:
        '''Get player hand.'''
        return self.__hand

    @hand.setter
    def hand(self, hand: Hand) -> None:
        '''Set player hand.'''
        self.__hand = hand

    @property
    def books(self) -> Set[Book]:
        '''Get awarded books.'''
        return self.__books

    @property
    def bid(self) -> Optional[int]:
        '''Get players bid.'''
        return self.__bid

    @bid.setter
    def bid(self, bid: int) -> None:
        '''Set players bid.'''
        self.__bid = bid

    def play_card(self, rank: str, suit: str) -> Optional[Card]:
        '''Play card from players hand.'''
        if self.__hand:
            return self.__hand.pull_card(rank, suit)
        else:
            raise exceptions.EmptyHandSizeException(
                'player has no cards to play'
            )

    def add_book(self, book: Book) -> None:
        '''Add book to players pile.'''
        self.__books.add(book)
