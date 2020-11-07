'''Provide book package.'''

from dataclass import dataclass


@dataclass
class Book:
    '''Provide book object.'''

    rank: str
    suit: str
