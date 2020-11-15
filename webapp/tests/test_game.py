# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

from random import randrange

import pytest

from spades import exceptions
from spades.game import Game
from spades.player import Player


game = Game()
game.add_player(Player('Jim'))
game.add_player(Player('Mike'))
game.add_player(Player('Jill'))
game.add_player(Player('Kim'))


def generate_bid(g: Game):
    turn = g.current_bidder()
    bid = randrange(0, 13)
    g.accept_bid(turn, bid)
    assert g.get_player(turn).bid == bid


def generate_trick(g: Game):
    turn = g.current_turn
    print('turn:', turn)
    player = g.get_player(turn)
    playable = player.hand.playable(g.stack.suit)
    card = [c for c in playable][0]
    g.play_trick(turn, card.rank, card.suit)
    # print('start hand:', game.get_player(turn).hand)


def test_game_states() -> None:
    '''Test game states.'''

    # test adding over maximum number of players.
    with pytest.raises(exceptions.InvalidPlayerException):
        game.add_player(Player('Jackson'))

    # while not game.check_winner():

    # start the game from waiting state
    assert game.state == 'waiting'
    game.start_game()

    # start accepting bids
    assert game.state == 'bidding'

    # ensure all bidders have been accounted for
    game.start_turn()
    assert game.state != 'playing'

    # TODO: switch to turn iterator
    for _ in [1, 2, 3, 4]:
        generate_bid(game)

    # check that no other bid can be made
    with pytest.raises(exceptions.IllegalBidException):
        game.accept_bid(game.current_bidder(), 2)

    while not game.check_handsize():
        # start player turns
        game.start_turn()
        assert game.state == 'playing'

        # check that all tricks have been accounted for
        game.end_turn()
        assert game.state != 'cleanup'

        # TODO: switch to turn iterator
        for x in [1, 2, 3, 4]:
            generate_trick(game)

            if x == 4 and len(game.get_player(game.current_turn).hand) > 0:
                with pytest.raises(exceptions.IllegalTurnException):
                    generate_trick(game)

        # end turn
        game.end_turn()
        assert game.state == 'cleanup'

        # ensure match cannot be ended with cards in hand
        game.end_match()
        if not game.check_handsize():
            assert game.state != 'waiting'
        else:
            assert game.state == 'waiting'
