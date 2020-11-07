'''Provide card package.'''

from dataclass import dataclass


@dataclass
class Card:
    '''Provide card object.'''

    rank: str
    suit: str
