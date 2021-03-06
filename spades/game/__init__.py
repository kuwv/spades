# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide game capabilities.'''

import logging
from random import randrange
from typing import List, Optional

from sqlalchemy.inspection import inspect
from transitions import Machine

from spades import config, db, exceptions
from spades.game.bid import BidMixin
from spades.game.models.book import Book
from spades.game.models.deck import Deck
from spades.game.models.hand import Hand
from spades.game.models.play import Play
from spades.game.models.player import Player
from spades.game.turn import PlayerTurns

log = logging.getLogger(__name__)
log.setLevel(config.loglevel)


class GameState(BidMixin, PlayerTurns):
    '''Provide game object.'''

    winning_score = config.winning_score

    states = [
        'waiting',
        'bidding',
        'playing',
        'cleanup',
    ]

    transitions = [
        {
            'trigger': 'start_game',
            'source': 'waiting',
            'before': 'select_dealer',
            'after': 'setup_game',
            'dest': 'bidding',
            'conditions': 'check_player_count'
        }, {
            'trigger': 'start_turn',
            'source': ['bidding', 'cleanup'],
            'before': 'setup_turn',
            'dest': 'playing',
            'conditions': 'check_bids'
        }, {
            'trigger': 'end_turn',
            'after': 'cleanup_turn',
            'source': 'playing',
            'dest': 'cleanup',
            'conditions': 'check_stack'
        }, {
            'trigger': 'end_match',
            'source': 'cleanup',
            'after': 'cleanup_match',
            'dest': 'waiting',
            'conditions': 'check_match'
        }, {
            'trigger': 'end_game',
            'source': '*',
            'dest': 'waiting',
            'conditions': 'check_winner'
        }
    ]

    def __init__(self, player_max: Optional[int] = None) -> None:
        '''Initialize game.'''
        super().__init__()
        if player_max:
            config.set_player_max(player_max)
        self.__dealer: Optional[int] = None
        self._bid_turn: int = 0
        self._deck: Deck = Deck()
        self.__stack: Optional[Book] = None

        self.machine = Machine(
            model=self,
            states=GameState.states,
            transitions=GameState.transitions,
            initial='waiting'
        )

    # statemachine

    def check_player_count(self) -> bool:
        '''Check player count state.'''
        return self.player_count == config.player_max

    def check_bids(self) -> bool:
        '''Check player bids state.'''
        count = 0
        for player in self.players:
            if player.bid is not None:
                log.debug(f"bid: {player.username} {player.bid}")
                count += 1
        check = True if count == config.player_max else False
        log.debug(f"check bids are set: {check}")
        return check

    def setup_turn(self) -> None:
        '''Run setup for dealer of next turn.'''
        if not self.__stack:
            self.__stack = Book()
            db.session.add(self.__stack)
            db.session.commit()
        if not self.current_turn:
            self.current_turn = self.dealer
        else:
            self.current_turn = self.current_turn % self.player_count

    def check_stack(self) -> bool:
        '''Check stack state.'''
        return True if len(self.stack) == self.player_count else False

    def cleanup_turn(self) -> None:
        '''Cleanup for next turn.'''
        if len(self.stack) == self.player_count:
            self.__award_book()
            self.current_turn = self.stack.winner
            self.__stack = None
        else:
            print('not ready to cleanup')

    def check_handsize(self) -> bool:
        '''Check if players hand state is empty.'''
        count = 0
        for player in self.players:
            if len(player.hand) == 0:
                count += 1
            log.debug(f"handsize: {player.username} {len(player.hand)}")
        return count == self.player_count

    def check_match(self) -> bool:
        '''Check if match state is finished.'''
        if self.check_handsize():
            for player in self.players:
                if len(player.hand) == 0:
                    return True
        return False

    def cleanup_match(self) -> None:
        '''Cleanup for next match.'''
        for player in self.players:
            player.score = True
        self.current_turn = self.dealer
        self._bid_turn = 0
        self._deck = Deck()

    def check_winner(self) -> bool:
        '''Check if score is a win.'''
        team1 = 0
        team2 = 0
        for x, player in enumerate(self.players):
            if x % 2 == 0:
                team1 += player.score
            else:
                team2 += player.score
        log.info(f"team1 score: {team1}")
        log.info(f"team2 score: {team2}")
        if team1 >= config.winning_score:
            return True
        if team2 >= config.winning_score:
            return True
        return False

    # statemachine end

    @property
    def dealer(self) -> Optional[int]:
        '''Get dealer.'''
        return self.__dealer

    def select_dealer(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count == config.player_max:
            if not self.dealer:
                self.__dealer = randrange(self.player_count)
            else:
                self.__dealer = (self.dealer + 1) % self.player_count
        log.debug(f"dealer: {self.dealer} {self.players[self.dealer].username}")

    def deal(self) -> None:
        '''Deal a new game.'''
        if self.state == 'bidding':  # type: ignore
            if self.player_count > 0:
                card_piles: List[Hand] = []
                for hand in range(0, 4):
                    card_piles.append(Hand())
                turn = 0
                for card in self._deck:
                    # TODO: if max hand less than 13
                    card_piles[turn % len(card_piles)].add_card(card)
                    turn += 1
                for player in self.players:
                    player.hand = card_piles.pop()
            else:
                raise exceptions.InvalidPlayerException('no players in game')
        else:
            raise exceptions.InvalidDeckException(
                'cannot deal hand during active game'
            )

    def setup_game(self) -> None:
        '''Run setup for a new game of spades.'''
        self.deal()
        # self.current_turn = 0

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < config.player_max:
                PlayerTurns.append_player(self, player)
            else:
                raise exceptions.InvalidPlayerException(
                    'max number of players registered'
                )
        else:
            raise exceptions.InvalidPlayerException(
                'cannot add player during game'
            )

    @property
    def stack(self):
        '''Get the current stack.'''
        return self.__stack

    def __award_book(self) -> None:
        '''Award book to player with trump or highest trick.'''
        if self.state == 'cleanup':
            player = self.get_player(self.stack.winner)
            # TODO: append stack
            player.books = self.stack
            log.info(f"LEAD: {self.stack.winner} {player.username}")
        else:
            raise exceptions.IllegalTurnException(
                'cannot award book during this phase'
            )

    def make_play(self, player_id: str, rank: str, suit: str) -> bool:
        '''Move player card to book.'''
        if self.state == 'playing':
            if player_id == self.current_turn:
                if len(self.stack) < self.player_count:
                    player = self.get_player(player_id)
                    print(player)
                    if (
                        len(self.__stack) == 0 or
                        suit == self.__stack.suit or
                        len(player.hand.list_suit(self.__stack.suit)) <= 0
                    ):
                        print('stack', self.__stack.id)
                        play = Play(
                            self.__stack.id,
                            player_id,
                            inspect(player.play_card(rank, suit)).identity[0]
                        )
                        db.session.add(play)
                        db.session.commit()
                        self.__stack.add_play(play)
                        db.session.add(player)
                        db.session.commit()
                        self.current_turn += 1
                    else:
                        raise exceptions.IllegalPlayException(
                            'cards of same suit must may be played'
                        )
                    log.info(f"play: {player.username} rank: {suit}")
                else:
                    raise exceptions.IllegalTurnException(
                        'current turn is already finished'
                    )
            else:
                raise exceptions.IllegalTurnException(
                    'players may only play during their turn'
                )
        else:
            raise exceptions.IllegalTurnException(
                'cannot play during other phase'
            )
