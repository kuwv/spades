# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide player capabilities.'''

from random import randrange

from typing import List, Optional

from spades import config
from spades import exceptions
from spades.models.player import Player


class PlayerTurns:
    '''Provide player turn object.'''

    def __init__(self, players: List[Player] = []) -> None:
        '''Initialize player turns.'''
        self.__players: List[Player] = players
        self.starting_turn = randrange(config.player_max)
        self.__turn = 0
        self.__current_turn = self.starting_turn

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
        '''Get players.'''
        return self.__players

    @property
    def player_count(self) -> int:
        '''Get number of current players.'''
        if self.__players:
            return len(self.__players)
        else:
            return 0

    @property
    def current_turn(self) -> int:
        '''Get turn of current player.'''
        return (self.__turn + self.__current_turn) % self.player_count

    @current_turn.setter
    def current_turn(self, turn: int) -> None:
        '''Set current total turn count.'''
        self.__current_turn = turn

    def append_player(self, player: Player) -> None:
        '''Add player to game.'''
        self.__players.append(player)

    def get_player(self, turn: int) -> Player:
        '''Get current player.'''
        return self.__players[turn % self.player_count]

    def get_player_by_username(self, username: str) -> Optional[Player]:
        '''Get current player by username.'''
        return next((p for p in self.__players if p.username == username), None)
