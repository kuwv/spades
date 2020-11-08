# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

from typing import List, Optional

from .book import Book
from .card import Card


class Hand:
    '''Provide player hand object.'''

    hand_size = 13

    def __init__(self) -> None:
        '''Initialize player hand.'''
        self.__hand: List[Card] = []

    def add_card(self, card: Card) -> None:
        '''Add card to player hand.'''
        self.__hand.append(card)

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
        self.__books: Book = []
        self.__bid: Optional[int] = None

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
        return self.hand.pull_card(rank, suit)

    def add_book(self, book):
        '''Add book to players pile.'''
        self.books.append(book)
