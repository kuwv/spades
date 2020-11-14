'''Provide game capabilities.'''

from typing import Optional

from spades import config
from spades import exceptions


class BidMixin:
    '''Provide setup object.'''

    @property
    def bid_turn(self) -> Optional[int]:
        '''Get current total turn count.'''
        if self._bid_turn:
            return self._bid_turn % config.player_max
        else:
            return self._bid_turn

    @bid_turn.setter
    def bid_turn(self, turn: int) -> None:
        '''Set current total turn count.'''
        self._bid_turn = turn

    @property
    def starting_bidder(self) -> int:
        '''Get current bidder.'''
        return (self.dealer + 1) % self.player_count

    def current_bidder(self) -> int:
        '''Get identity of current bidder.'''
        return (self.bid_turn + self.starting_bidder) % config.player_max

    def current_bidder_name(self, turn: int) -> str:
        '''Get current bidder name.'''
        return self.players[turn].name

    def accept_bid(self, player_id: int, bid: int) -> bool:
        '''Accpet bids from players.'''
        if self.state == 'bidding':
            if player_id == self.current_bidder():
                if self._bid_turn < config.player_max:
                    print(self.current_bidder_name(player_id), bid)
                    self.players[player_id].bid = bid
                    self.bid_turn += 1
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
        return True if count == config.player_max else False