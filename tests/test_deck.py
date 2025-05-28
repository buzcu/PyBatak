import pytest
import sys
sys.path.append("../batak")
from deck import Deck
from card import Card

@pytest.fixture
def fresh_deck():
    """Fixture to provide a new deck for each test."""
    return Deck()

def test_deck_initialization(fresh_deck):
    """Test that a new deck has 52 cards."""
    assert len(fresh_deck) == 52

def test_deck_build(fresh_deck):
    """Test that all 52 cards are unique and valid."""
    suits = {"Hearts", "Diamonds", "Clubs", "Spades"}
    ranks = set(range(2, 15))
    seen_cards = set()

    for card in fresh_deck.cards:
        assert card.suit in suits
        assert card.rank in ranks
        seen_cards.add((card.suit, card.rank))

    assert len(seen_cards) == 52

def test_shuffle(fresh_deck):
    """Test that shuffling changes the order."""
    original_order = fresh_deck.cards.copy()
    fresh_deck.shuffle()
    assert original_order != fresh_deck.cards
    assert len(fresh_deck) == 52

def test_deal(fresh_deck):
    """Test dealing cards."""
    dealt_cards = fresh_deck.deal(5)
    assert len(dealt_cards) == 5
    assert len(fresh_deck) == 47

    for card in dealt_cards:
        #assert card not in fresh_deck.cards
        print(f"Dealt card: {card}")
    for card in fresh_deck.cards:
        #assert card not in dealt_cards
        print(f"Remaining card: {card}")
    for card in dealt_cards:
        assert card not in fresh_deck.cards

""" def test_deal_removes_cards(fresh_deck):
    dealt_cards = fresh_deck.deal(5)
    assert len(fresh_deck) == 47

    # Check dealt cards are gone
    for card in dealt_cards:
        assert card not in fresh_deck.cards

    # Check remaining cards are correct
    for card in fresh_deck.cards:
        assert card not in dealt_cards """

def test_deal_too_many(fresh_deck):
    """Test dealing more cards than available."""
    with pytest.raises(ValueError):
        fresh_deck.deal(53)

def test_repr(fresh_deck):
    """Test the deck's string representation."""
    assert repr(fresh_deck) == "Deck(52 cards remaining)"
    fresh_deck.deal(10)
    assert repr(fresh_deck) == "Deck(42 cards remaining)"