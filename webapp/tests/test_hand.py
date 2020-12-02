# type: ignore
'''Test hand.'''

from spades.models.card import Card
from spades.models.player import Hand


def test_hand() -> None:
    hand = Hand()
    hand.add_card(Card('A', 'S'))
    card = hand.pull_card('A', 'S')
    assert card.rank == 'A'
    assert card.suit == 'S'
