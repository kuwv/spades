'''Test hand.'''

from spades.card import Card
from spades.player import Hand


def test_hand() -> None:
    hand = Hand()
    hand.add_card(Card('A', 'Spades'))
    card = hand.pull_card('A', 'Spades')
    assert card.rank == 'A'  # type: ignore
    assert card.suit == 'Spades'  # type: ignore
