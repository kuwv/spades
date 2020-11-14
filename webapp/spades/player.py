# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

from random import randrange

from typing import List, Optional, Set

from spades import config
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


class PlayerTurns:
    '''Provide player turn object.'''

    def __init__(self, players: List[Player] = []) -> None:
        '''Initialize player turns.'''
        self.__players: List[Player] = players
        self.starting_turn = randrange(config.player_max)
        self.__turn = self.starting_turn

    def __iter__(self) -> 'PlayerTurns':
        '''Return self as iterator.'''
        self.__turn = 0
        return self

    def __next__(self) -> Player:
        '''Get next player instance.'''
        if self.__turn >= self.player_count:
            raise exceptions.StopIteration()
        player = self.__players[self.current_turn]
        self.__turn += 1
        return player

    @property
    def players(self) -> List[Player]:
        return self.__players

    @property
    def player_count(self) -> int:
        '''Get number of current players.'''
        if self.__players:
            return len(self.__players)
        else:
            return 0

    @property
    def starting_turn(self) -> None:
        '''Get current player turn.'''
        return self.__current_turn

    @starting_turn.setter
    def starting_turn(self, turn: int) -> None:
        '''Set current player turn.'''
        self.__current_turn = turn

    @property
    def current_turn(self) -> int:
        '''Get turn of current player.'''
        return (self.__turn + self.__current_turn) % self.player_count

    def append_player(self, player: Player) -> None:
        '''Add player to game.'''
        self.__players.append(player)

    def get_player(self, number: int) -> Player:
        '''Get current player.'''
        return self.__players[number % self.player_count]

    def get_player_by_name(self, name: str) -> Optional[Player]:
        '''Get current player by name.'''
        return next((p for p in self.__players if p.name == name), None)
