# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

from typing import List, Optional, Set

from .book import Book
from .card import Card
from .exceptions import EmptyHandSizeException, MaxHandSizeException


class Hand:
    '''Provide player hand object.'''

    max_size = 13

    def __init__(self) -> None:
        '''Initialize player hand.'''
        self.__hand: List[Card] = []

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        if len(self.__hand) < Hand.max_size:
            self.__hand.append(card)
        else:
            raise MaxHandSizeException('maximum hand size')

    def pull_card(self, rank: str, suit: str) -> Optional[Card]:
        selection = Card(rank, suit)
        for card in self.__hand:
            if selection == card:
                return card
        return None


class Player:
    '''Provide player object.'''

    def __init__(self, name: str) -> None:
        '''Initialize player.'''
        self.name = name
        self.__hand: Optional[Hand] = None
        self.__books: Set[Book] = Set()
        self.__bid: Optional[int] = None

    @property
    def books(self) -> Set[Book]:
        return self.__books

    @property
    def bid(self) -> Optional[int]:
        '''Get players bid.'''
        return self.__bid

    @bid.setter
    def bid(self, bid: int) -> None:
        '''Set players bid.'''
        if self.__bid is None:
            self.__bid = bid

    def add_hand(self, hand: Hand) -> None:
        if not self.__hand:
            self.__hand = hand

    def play_card(self, rank: str, suit: str) -> Optional[Card]:
        '''Play card from players hand.'''
        if self.__hand:
            return self.__hand.pull_card(rank, suit)
        else:
            raise EmptyHandSizeException('player has no cards to play')

    def add_book(self, book: Book) -> None:
        '''Add book to players pile.'''
        self.__books.add(book)
