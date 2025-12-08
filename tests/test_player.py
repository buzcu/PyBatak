import pytest
import sys

sys.path.append("..")
from batak import Player
from batak import Card
from unittest.mock import patch


@pytest.fixture
def sample_hand():
    return [
        Card("Hearts", 14),  # Ace
        Card("Hearts", 13),  # King
        Card("Spades", 11),  # Jack
        Card("Clubs", 9),
        Card("Diamonds", 7),
    ]


@pytest.fixture
def sample_full_hand():
    return [
        Card("Hearts", 3),
        Card("Hearts", 4),
        Card("Spades", 11),
        Card("Clubs", 9),
        Card("Hearts", 7),
        Card("Clubs", 9),
        Card("Clubs", 11),
        Card("Clubs", 12),
        Card("Clubs", 10),
        Card("Diamonds", 7),
        Card("Spades", 5),
        Card("Diamonds", 11),
        Card("Spades", 7),
    ]

@pytest.fixture
def bot_player(sample_hand):
    return Player("BotPlayer", is_bot=True, hand=sample_hand.copy())

@pytest.fixture
def bot_player2(sample_full_hand):
    return Player("BotPlayer2", is_bot=True, hand=sample_full_hand.copy())

@pytest.fixture
def human_player(sample_hand):
    return Player("HumanPlayer", is_bot=False, hand=sample_hand.copy())


def test_number_of_cards_in_suit(bot_player):
    assert bot_player.number_of_cards_in_suit("Hearts") == 2
    assert bot_player.number_of_cards_in_suit("Spades") == 1
    assert bot_player.number_of_cards_in_suit("Clubs") == 1
    assert bot_player.number_of_cards_in_suit("Diamonds") == 1


def test_simple_trump_logic_2(bot_player2):
    trump = bot_player2.simple_trump_logic()
    assert trump == "Clubs"  # BotPlayer2 has the most Clubs cards


def test_simple_bid_logic(bot_player2):
    bid = bot_player2.simple_bid_logic()
    assert isinstance(bid, int)
    assert 5 <= bid <= 13


@patch("builtins.input", return_value="7")
def test_bid_user_input(mock_input, human_player):
    assert human_player.bid() == 7


def test_bot_bid(bot_player):
    bid = bot_player.bid()
    assert isinstance(bid, int)


@patch("builtins.input", side_effect=["Hearts"])
def test_choose_trump_valid(mock_input, human_player):
    assert human_player.choose_trump() == "Hearts"


@patch("builtins.input", side_effect=["Invalid", "Clubs"])
def test_choose_trump_retry_on_invalid(mock_input, human_player):
    assert human_player.choose_trump() == "Clubs"


def test_simple_trump_logic(bot_player):
    trump = bot_player.simple_trump_logic()
    assert trump in ["Hearts", "Spades", "Clubs", "Diamonds"]


def test_bot_play_card_logic(bot_player):
    cards_on_table = [Card("Clubs", 10)]
    trump_suit = "Spades"
    legal_cards = [card for card in bot_player.hand if card.suit == "Clubs"]
    if not legal_cards:
        legal_cards = bot_player.hand.copy()

    card_played = bot_player.play_card(cards_on_table, trump_suit, legal_cards)
    assert isinstance(card_played, Card)
    assert card_played not in bot_player.hand


@patch("builtins.input", return_value="0")
def test_human_play_card(mock_input, human_player):
    cards_on_table = [Card("Clubs", 10)]
    trump_suit = "Hearts"
    legal_cards = human_player.hand[:2]
    chosen_card = human_player.play_card(cards_on_table, trump_suit, legal_cards)
    assert chosen_card == legal_cards[0]
    assert chosen_card not in human_player.hand
