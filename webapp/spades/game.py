'''Provide game capabilities.'''

from random import randrange
from typing import List, Optional

from transitions import Machine

from spades.book import Book
from spades.card import Card
from spades.deck import Deck
from spades.exceptions import (
    IllegalBidException,
    IllegalDeckException,
    IllegalPlayerException,
    IllegalTurnException,
    MaxPlayerException,
    NoPlayerException
)
from spades.hand import Hand
from spades.player import Player


class SetupMixin:
    '''Provide setup object.'''

    @property
    def starting_bidder(self) -> int:
        '''Get current bidder.'''
        return (self.dealer + 1) % self.player_count

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
                for player in self._players:
                    player.hand = card_piles.pop()
            else:
                raise NoPlayerException('no players in game')
        else:
            raise IllegalDeckException('cannot deal hand during active game')

    def select_dealer(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count == Game.player_max:
            if not self.dealer:
                self.dealer = randrange(self.player_count)
            else:
                self.dealer = (self.dealer + 1) % self.player_count
        print('dealer:', self.dealer, self._players[self.dealer].name)

    def current_bidder(self) -> int:
        '''Get identity of current bidder.'''
        return (self.current_turn + self.starting_bidder) % Game.player_max

    def current_bidder_name(self, turn: int) -> str:
        return self._players[turn].name

    def take_bid(self, player_id: int, bid: int) -> bool:
        if self.state == 'bidding':
            if player_id == self.current_bidder():
                if self._current_turn < Game.player_max:
                    print(
                        self.current_bidder_name(player_id),
                        bid
                    )
                    self._players[player_id].bid = bid
                    self.current_turn += 1
                else:
                    raise IllegalBidException('no additional bids can be made')
            else:
                raise IllegalBidException(
                    'cannot bid during other players turn'
                )
        else:
            raise IllegalTurnException('cannot bid during this phase')

    def check_bids(self) -> bool:
        '''Check player bids.'''
        count = 0
        for player in self._players:
            if player.bid:
                count += 1
        return True if count == Game.player_max else False

    def setup_game(self) -> None:
        '''Setup a new game of spades.'''
        self.deal()
        self._current_turn = 0


class PlayerTurn:
    '''Provide turn object.'''

    def __init__(self, players: List[Player]) -> None:
        '''Initialize Deck.'''
        self.__players: List[Player] = players

    def __iter__(self) -> 'PlayerTurn':
        '''Return itself as iterator.'''
        return self

    def __next__(self) -> Card:
        '''Get next player instance.'''
        if len(self.__players) <= Game.player_max:
            raise StopIteration()
        return self.__players.pop()


class Game(SetupMixin):
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
            'before': 'select_dealer',
            'after': 'setup_game',
            'dest': 'bidding',
            'conditions': 'check_player_count'
        }, {
            'trigger': 'start_turn',
            'source': ['bidding', 'cleanup'],
            'before': 'select_leader',
            'dest': 'playing',
            'conditions': 'check_bids'
        }, {
            'trigger': 'end_turn',
            'source': 'playing',
            'dest': 'cleanup'
        }, {
            'trigger': 'end_match',
            'source': 'cleanup',
            'dest': ['playing', 'waiting'],
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
        self.dealer: Optional[int] = None
        # self._current_turn: Optional[int] = None
        self._current_turn: int = 0
        self._current_leader: Optional[int] = None
        self.deck: Deck = Deck()
        self._players: List[Player] = []

        self.machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='waiting'
        )

    @property
    def player_count(self) -> int:
        '''Get player count.'''
        return len(self._players)

    @property
    def current_turn(self) -> Optional[int]:
        '''Get current total turn count.'''
        if self._current_turn:
            return self._current_turn % Game.player_max
        else:
            return self._current_turn

    @current_turn.setter
    def current_turn(self, turn: int) -> None:
        '''Set current total turn count.'''
        self._current_turn = turn

    @property
    def current_leader(self) -> None:
        '''Get current player turn.'''
        return self._current_leader

    @current_leader.setter
    def current_leader(self, turn: int) -> None:
        '''Set current player turn.'''
        self._current_leader = turn

    def get_player(self, number: int) -> Player:
        '''Get current player.'''
        return self._players[number % self.player_count]

    def get_player_by_name(self, name: str) -> Optional[Player]:
        return next((p for p in self._players if p.name == name), None)

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < Game.player_max:
                self._players.append(player)
            else:
                raise MaxPlayerException('max number of players registered')
        else:
            raise IllegalPlayerException('cannot add player active game')

    def take_player_card(self, player_id: str, card: Card) -> bool:
        '''Move player card to book.'''
        if self.state == 'playing':
            pass
        else:
            raise IllegalTurnException('cannot play during this phase')

    def award_book(self, player: Player, book: Book) -> None:
        '''Award book to player with trump or highest trick.'''
        if self.state == 'cleanup':
            pass
        else:
            raise IllegalTurnException('cannot award book during this phase')

    def select_leader(self) -> Optional[bool]:
        # True if self._current_leader else False
        if not self.current_leader:
            self.current_leader = self.dealer
        else:
            self.current_leader = (self.current_leader + 1) % self.player_count

    # state checks

    def check_player_count(self) -> bool:
        return self.player_count == Game.player_max

    def check_player_turn(self, player_id: str) -> bool:
        return player_id == self._players[player_id]

    def check_hands(self) -> bool:
        '''Check player hands.'''
        count = 0
        for player in self._players:
            if len(player.hand) == 0:
                count += 1
        return count == Game.player_max

    def check_match(self) -> bool:
        '''Check if match is finished.'''
        if self.check_hands:
            for player in self._players:
                if len(player.hand) == 0:
                    return True
        return False

    def check_winner(self) -> bool:
        '''Check if number of points is a win.'''
        # for player in self._players:
        #     if player
        return False
