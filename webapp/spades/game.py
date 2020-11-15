# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide game capabilities.'''

import logging
from random import randrange
from typing import List, Optional

from transitions import Machine

from spades import config
from spades import exceptions
from spades.bid import BidMixin
from spades.book import Book
from spades.deck import Deck
from spades.hand import Hand
from spades.player import Player
from spades.turn import PlayerTurns

# logger = logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(config.loglevel)


class Game(BidMixin, PlayerTurns):
    '''Provide game object.'''

    player_max = config.player_max
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

    def __init__(self) -> None:
        '''Initialize game.'''
        super().__init__()
        self.__dealer: Optional[int] = None
        self._bid_turn: int = 0
        self._deck: Deck = Deck()
        self.__stack: Book = None

        self.machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='waiting'
        )

    # statemachine

    def check_player_count(self) -> bool:
        return self.player_count == Game.player_max

    def check_bids(self) -> bool:
        '''Check player bids.'''
        count = 0
        for player in self.players:
            if player.bid is not None:
                log.debug(f"bid: {player.name} {player.bid}")
                count += 1
        check = True if count == config.player_max else False
        log.debug(f"check bids are set: {check}")
        return check

    def setup_turn(self) -> None:
        if not self.__stack:
            self.__stack = Book()

        # TODO this should pick last winner
        if not self.current_turn:
            self.current_turn = self.dealer
        else:
            self.current_turn = self.current_turn % self.player_count

    def check_stack(self) -> bool:
        return True if len(self.stack) == self.player_count else False

    def cleanup_turn(self) -> None:
        if len(self.stack) == self.player_count:
            self.__award_book()
            self.current_turn = self.stack.winner
            self.__stack = None
        else:
            print('do something')

    def check_handsize(self) -> bool:
        count = 0
        for player in self.players:
            if len(player.hand) == 0:
                count += 1
            log.debug(f"handsize: {player.name} {len(player.hand)}")
        return count == self.player_count

    def check_match(self) -> bool:
        '''Check if match is finished.'''
        if self.check_handsize():
            for player in self.players:
                if len(player.hand) == 0:
                    return True
        return False

    def cleanup_match(self) -> None:
        '''Cleanup bids.'''
        # print('cleanup match')
        for player in self.players:
            print(player.name, len(player.books), player.bid, player.score)
            player.score = True
            print(player.name, player.score)
        self.current_turn = self.dealer
        self._bid_turn = 0
        self._deck = Deck()
        # print('cleanup match end')

    def check_winner(self) -> bool:
        '''Check if score is a win.'''
        # print('check winner')
        team1 = 0
        team2 = 0
        for x, player in enumerate(self.players):
            if x % 2 == 0:
                team1 += player.score
            else:
                team2 += player.score
        log.info(f"team1 score: {team1}")
        print(f"team1 score: {team1}")
        log.info(f"team2 score: {team2}")
        print(f"team2 score: {team2}")
        if team1 >= config.winning_score:
            return True
        if team2 >= config.winning_score:
            return True
        # print('check winner end''')
        return False

    # statemachine end

    @property
    def dealer(self) -> Optional[int]:
        '''Get dealer.'''
        return self.__dealer

    def select_dealer(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count == Game.player_max:
            if not self.dealer:
                self.__dealer = randrange(self.player_count)
            else:
                self.__dealer = (self.dealer + 1) % self.player_count
        log.debug(f"dealer: {self.dealer} {self.players[self.dealer].name}")

    def deal(self) -> None:
        '''Deal a new game.'''
        if self.state == 'bidding':  # type: ignore
            if self.player_count > 0:
                card_piles: List[Hand] = []
                for hand in range(0, self.player_count):
                    card_piles.append(Hand())
                turn = 0
                for card in self._deck:
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
        '''Setup a new game of spades.'''
        self.deal()
        # self.current_turn = 0

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < Game.player_max:
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
        return self.__stack

    def __award_book(self) -> None:
        '''Award book to player with trump or highest trick.'''
        if self.state == 'cleanup':
            player = self.get_player(self.stack.winner)
            player.books = self.stack
            log.info(f"LEAD: {self.stack.winner} {player.name}")
        else:
            raise exceptions.IllegalTurnException(
                'cannot award book during this phase'
            )

    def play_trick(self, player_id: str, rank: str, suit: str) -> bool:
        '''Move player card to book.'''
        if self.state == 'playing':
            if player_id == self.current_turn:
                if len(self.stack) < self.player_count:
                    player = self.get_player(player_id)
                    if (
                        len(self.__stack) == 0 or
                        suit == self.__stack.suit or
                        len(player.hand.list_suit(self.__stack.suit)) <= 0
                    ):
                        self.__stack.add_trick(
                            player_id,
                            player.play_card(rank, suit)
                        )
                        self.current_turn += 1
                    else:
                        raise exceptions.IllegalPlayException(
                            'cards of same suit must may be played'
                        )
                    log.info(f"play: {player.name} rank: {suit}")
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
