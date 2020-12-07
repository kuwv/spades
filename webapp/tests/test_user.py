# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for players.'''

# import pytest

from spades.models.user import User


def test_password():
    '''Test user passwords.'''
    user = User(username='test')
    user.set_password('password')
    assert user.check_password('password')


# def test_turn() -> None:
#     player_turns = PlayerTurns()
#     player_turns.add_player(Player('Jim'))
#     player_turns.add_player(Player('Mike'))
#     player_turns.add_player(Player('Jill'))
#     player_turns.add_player(Player('Kim'))
#     for player in player_turns:
#         print('username:', player.username)
#
#     turns = iter(player_turns)
#     player_one = next(turns)
#     print(player_one)
