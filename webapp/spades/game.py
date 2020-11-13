'''Provide game capabilities.'''

from random import randrange
from typing import List, Optional

from transitions import Machine

from spades import exceptions
from spades.book import Book
from spades.card import Card
from spades.deck import Deck
from spades.hand import Hand
from spades.player import Player


class SetupMixin:
    '''Provide setup object.'''

    # ***************************************
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
    # ***************************************

    @property
    def starting_bidder(self) -> int:
        '''Get current bidder.'''
        return (self.dealer + 1) % self.player_count

    def current_bidder(self) -> int:
        '''Get identity of current bidder.'''
        return (self.current_turn + self.starting_bidder) % Game.player_max

    def current_bidder_name(self, turn: int) -> str:
        return self.players[turn].name

    def take_bid(self, player_id: int, bid: int) -> bool:
        if self.state == 'bidding':
            if player_id == self.current_bidder():
                if self._current_turn < Game.player_max:
                    print(self.current_bidder_name(player_id), bid)
                    self.players[player_id].bid = bid
                    self.current_turn += 1
                else:
                    raise exceptions.IllegalBidException(
                        'no additional bids can be made'
                    )
            else:
                raise exceptions.IllegalBidException(
                    'cannot bid during other players turn'
                )
        else:
            raise exceptions.IllegalTurnException(
                'cannot bid during this phase'
            )

    def check_bids(self) -> bool:
        '''Check player bids.'''
        count = 0
        for player in self.players:
            if player.bid:
                count += 1
        return True if count == Game.player_max else False

    def setup_game(self) -> None:
        '''Setup a new game of spades.'''
        self.deal()
        self._current_turn = 0


class PlayerTurns:
    '''Provide player turn object.'''

    def __init__(self, players: List[Player] = []) -> None:
        '''Initialize player turns.'''
        self.__players: List[Player] = players
        self.__current = randrange(Game.player_max)

    def __iter__(self) -> 'PlayerTurns':
        '''Return self as iterator.'''
        self.__turn = 0
        return self

    def __next__(self) -> Player:
        '''Get next player instance.'''
        if self.__turn >= self.player_count:
            raise exceptions.StopIteration()
        player = self.__players[self.current]
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
    def current(self) -> int:
        '''Get turn of current player.'''
        return (self.__turn + self.__current) % self.player_count

    @current.setter
    def current(self, turn: int):
        '''Set turn of current player.'''
        self.__current = turn

    def append_player(self, player: Player) -> None:
        '''Add player to game.'''
        self.__players.append(player)

    def get_player(self, number: int) -> Player:
        '''Get current player.'''
        return self.__players[number % self.player_count]

    def get_player_by_name(self, name: str) -> Optional[Player]:
        return next((p for p in self.__players if p.name == name), None)


class Game(PlayerTurns, SetupMixin):
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
        super().__init__()
        self.dealer: Optional[int] = None
        # self._current_turn: Optional[int] = None
        self._current_turn: int = 0
        self._current_leader: Optional[int] = None
        self.deck: Deck = Deck()

        self.machine = Machine(
            model=self,
            states=Game.states,
            transitions=Game.transitions,
            initial='waiting'
        )

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
                for player in self.players:
                    player.hand = card_piles.pop()
            else:
                raise exceptions.NoPlayerException('no players in game')
        else:
            raise exceptions.IllegalDeckException(
                'cannot deal hand during active game'
            )

    def select_dealer(self) -> None:
        '''Randomly choose starting player.'''
        if self.player_count == Game.player_max:
            if not self.dealer:
                self.dealer = randrange(self.player_count)
            else:
                self.dealer = (self.dealer + 1) % self.player_count
        print('dealer:', self.dealer, self.players[self.dealer].name)

    def add_player(self, player: Player) -> None:
        '''Add player to game.'''
        if self.state == 'waiting':  # type: ignore
            if self.player_count < Game.player_max:
                PlayerTurns.append_player(self, player)
            else:
                raise exceptions.MaxPlayerException(
                    'max number of players registered'
                )
        else:
            raise exceptions.IllegalPlayerException(
                'cannot add player active game'
            )

    def take_player_card(self, player_id: str, card: Card) -> bool:
        '''Move player card to book.'''
        if self.state == 'playing':
            pass
        else:
            raise exceptions.IllegalTurnException(
                'cannot play during this phase'
            )

    def award_book(self, player: Player, book: Book) -> None:
        '''Award book to player with trump or highest trick.'''
        if self.state == 'cleanup':
            pass
        else:
            raise exceptions.IllegalTurnException(
                'cannot award book during this phase'
            )

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
        return player_id == self.players[player_id]

    def check_hands(self) -> bool:
        '''Check player hands.'''
        count = 0
        for player in self.players:
            if len(player.hand) == 0:
                count += 1
        return count == self.player_count

    def check_match(self) -> bool:
        '''Check if match is finished.'''
        if self.check_hands:
            for player in self.players:
                if len(player.hand) == 0:
                    return True
        return False

    def check_winner(self) -> bool:
        '''Check if number of points is a win.'''
        # for player in self.players:
        #     if player
        return False
