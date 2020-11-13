# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

import pytest

# from spades import exceptions
from spades.game import Game, PlayerTurn
from spades.player import Player


def test_turn() -> None:
    player_turns = PlayerTurn()
    player_turns.add_player(Player('Jim'))
    player_turns.add_player(Player('Mike'))
    player_turns.add_player(Player('Jill'))
    player_turns.add_player(Player('Kim'))
    for player in player_turns:
        print('name:', player.name)

    turns = iter(player_turns)
    player_one = next(turns)
    print(player_one)
