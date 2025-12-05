import pytest
import sys
sys.path.append("..")
from batak import Card

@pytest.fixture
def test_cards():
    return {
        "ace_spades": Card("Spades", 14),
        "king_hearts": Card("Hearts", 13),
        "two_clubs": Card("Clubs", 2),
    }

def test_init(test_cards):
    assert test_cards["ace_spades"].rank == 14
    assert test_cards["king_hearts"].suit == "Hearts"

    with pytest.raises(ValueError):
        Card("Spades", 0)  # Invalid rank (too low)
    with pytest.raises(ValueError):
        Card("InvalidSuit", 10)  # Invalid suit

def test_repr(test_cards):
    assert str(test_cards["ace_spades"]) == "A of Spades"
    assert str(test_cards["king_hearts"]) == "K of Hearts"
    assert str(test_cards["two_clubs"]) == "2 of Clubs"

def test_equality(test_cards):
    same_as_ace = Card("Spades", 14)
    assert test_cards["ace_spades"] == same_as_ace
    assert test_cards["ace_spades"] != test_cards["king_hearts"]

def test_comparison(test_cards):
    assert test_cards["two_clubs"] < test_cards["king_hearts"]
    assert test_cards["king_hearts"] > test_cards["two_clubs"]
    assert test_cards["ace_spades"] >= Card("Spades", 14)

def test_hash(test_cards):
    card_set = {test_cards["ace_spades"], test_cards["king_hearts"]}
    assert test_cards["ace_spades"] in card_set

def test_get_value_and_suit(test_cards):
    assert test_cards["king_hearts"].rank == 13
    assert test_cards["king_hearts"].suit == "Hearts"