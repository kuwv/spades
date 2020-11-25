# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide tests for game.'''

import pytest

from spades import exceptions
from spades.game import Game
from spades.models.player import Player


game = Game()
game.add_player(Player('Jim'))
game.add_player(Player('Mike'))
game.add_player(Player('Jill'))
game.add_player(Player('Kim'))


def generate_bid(g: Game):
    turn = g.current_bidder()
    player = g.get_player(turn)
    bid = len(player.hand.list_suit('Spades'))
    g.accept_bid(turn, bid)
    assert player.bid == bid


def generate_trick(g: Game):
    turn = g.current_turn
    # print('turn:', turn)
    player = g.get_player(turn)
    playable = player.hand.playable(g.stack.suit)
    card = [c for c in playable][0]
    g.play_trick(turn, card.rank, card.suit)
    # print(f"{player.username} hand: {player.hand}")


def test_game_states() -> None:
    '''Test game states.'''

    # test adding over maximum number of players.
    with pytest.raises(exceptions.InvalidPlayerException):
        game.add_player(Player('Jackson'))

    count = 0
    while not game.check_winner():
        print('start new match')

        # start the game from waiting state
        assert game.state == 'waiting'
        # print(f"{game.state} == waiting")

        # start accepting bids
        game.start_game()
        assert game.state == 'bidding'
        # print(f"{game.state} == bidding")

        # ensure all bidders have been accounted for
        game.start_turn()
        assert game.state != 'playing'
        # print(f"{game.state} != playing")

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

                if x == 4 and len(
                    game.get_player(game.current_turn).hand
                ) > 0:
                    with pytest.raises(exceptions.IllegalTurnException):
                        generate_trick(game)

            # end turn
            game.end_turn()
            assert game.state == 'cleanup'

            # ensure match cannot be ended with cards in hand
            game.end_match()
            if not game.check_handsize():
                # print('not waiting')
                assert game.state != 'waiting'
            else:
                # print('wating now')
                assert game.state == 'waiting'
        count += 1
        print('match count:', count)

        game.end_game()
    assert game.state == 'waiting'
