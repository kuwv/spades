'''Provide book package.'''

from dataclasses import dataclass


@dataclass
class Book:
    '''Provide book object.'''

    rank: str
    suit: str
