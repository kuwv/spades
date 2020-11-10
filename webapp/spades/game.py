'''Provide game capabilities.'''

from random import randrange
from typing import List

from transitions import Machine

from .book import Book
from .deck import Deck
from .exceptions import (
    IllegalDeckException,
    IllegalPlayerException,
    MaxPlayersException,
    NoPlayersException
)
from .hand import Hand
from .player import Player


class Game:
    '''Provide game object.'''

    player_max = 4
    winning_points = 200

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
            'before': 'set_start_player',
            'after': 'deal',
            'dest': 'bidding'
        }, {
            'trigger': 'start_match',
            'source': ['bidding', 'cleanup'],
            'dest': 'playing',
            'conditions': 'check_bids'
        }, {
            'trigger': 'player_turn',
            'source': 'playing',
            'dest': 'cleanup'
        }, {
            'trigger': 'end_turn',
            'source': 'playing',
            'dest': 'cleanup'
            # }, {
            #     'trigger': 'end_match',
            #     'source': 'end_turn',
            #     'dest': ['new_match', 'end_game'],
            #     'conditions': 'check_hand_size'
            # }, {
            #     'trigger': 'end_game',
            #     'source': '*',
            #     'dest': 'waiting',
            #     # 'conditions': 'check_points'
        }
    ]

    def __init__(
        self,
        starting_player: int = None,
    ) -> None:
        '''Initialize game.'''
        self.player_turn: int = 0
        self.deck: Deck = Deck()
        self.__players: List[Player] = []

        self.machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='waiting'
        )

    @property
    def player_count(self) -> int:
        '''Get player count.'''
        return len(self.__players)

    @property
    def current_player(self) -> Player:
        '''Get current player.'''
        return self.__players[self.player_turn % self.player_count]

    def set_start_player(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count != 0:
            self.player_turn = randrange(self.player_count)
        print(self.player_turn)

    def next_player(self) -> None:
        pass

    def deal(self) -> None:
        '''Deal a new game.'''
        if self.state == 'bidding':  # type: ignore
            if self.player_count > 0:
                card_piles: List[Hand] = []
                for hand in range(0, self.player_count):
                    card_piles.append(Hand())

                turn = 0
                for card in self.deck:
                    card_piles[turn % len(card_piles)].add_card(card)
                    turn += 1

                for player in self.__players:
                    player.hand = card_piles.pop()
            else:
                raise NoPlayersException('no players in game')
        else:
            raise IllegalDeckException('cannot deal hand during active game')

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < Game.player_max:
                self.__players.append(player)
            else:
                raise MaxPlayersException('max number of players')
        else:
            raise IllegalPlayerException('game has already started')

    def award_book(self, player: Player, book: Book) -> None:
        # self.books.append(book)
        pass

    def check_bids(self) -> bool:
        return True

    def check_hand_size(self) -> bool:
        return False

    def check_points(self) -> bool:
        return False
