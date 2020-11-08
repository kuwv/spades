'''Test hand.'''

from spades.card import Card
from spades.player import Hand


def test_hand():
    hand = Hand()
    hand.add_card(Card('A', 'Spades'))
    card = hand.pull_card('A', 'Spades')
    assert card.rank == 'A'
    assert card.suit == 'Spades'
