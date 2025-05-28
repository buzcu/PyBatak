import pytest
import sys
sys.path.append("../batak")
from player import Player
from card import Card
from unittest.mock import patch


@pytest.fixture
def sample_hand():
    return [
        Card('Hearts', 14),    # Ace
        Card('Hearts', 13),    # King
        Card('Spades', 11),    # Jack
        Card('Clubs', 9),
        Card('Diamonds', 7)
    ]

@pytest.fixture
def bot_player(sample_hand):
    return Player("BotPlayer", is_bot=True, hand=sample_hand.copy())

@pytest.fixture
def human_player(sample_hand):
    return Player("HumanPlayer", is_bot=False, hand=sample_hand.copy())


def test_number_of_cards_in_suit(bot_player):
    assert bot_player.number_of_cards_in_suit('Hearts') == 2
    assert bot_player.number_of_cards_in_suit('Spades') == 1
    assert bot_player.number_of_cards_in_suit('Clubs') == 1
    assert bot_player.number_of_cards_in_suit('Diamonds') == 1



def test_simple_bid_logic(bot_player):
    bid = bot_player.simple_bid_logic()
    assert isinstance(bid, int)
    assert 5 <= bid <= 13


@patch('builtins.input', return_value='7')
def test_bid_user_input(mock_input, human_player):
    assert human_player.bid() == 7


def test_bot_bid(bot_player):
    bid = bot_player.bid()
    assert isinstance(bid, int)


@patch('builtins.input', side_effect=['Hearts'])
def test_choose_trump_valid(mock_input, human_player):
    assert human_player.choose_trump() == 'Hearts'


@patch('builtins.input', side_effect=['Invalid', 'Clubs'])
def test_choose_trump_retry_on_invalid(mock_input, human_player):
    assert human_player.choose_trump() == 'Clubs'


def test_simple_trump_logic(bot_player):
    trump = bot_player.simple_trump_logic()
    assert trump in ['Hearts', 'Spades', 'Clubs', 'Diamonds']


def test_bot_play_card_logic(bot_player):
    cards_on_table = [Card('Clubs', 10)]
    trump_suit = 'Spades'
    legal_cards = [card for card in bot_player.hand if card.suit == 'Clubs']
    if not legal_cards:
        legal_cards = bot_player.hand.copy()

    card_played = bot_player.play_card(cards_on_table, trump_suit, legal_cards)
    assert isinstance(card_played, Card)
    assert card_played not in bot_player.hand


@patch('builtins.input', return_value='0')
def test_human_play_card(mock_input, human_player):
    cards_on_table = [Card('Clubs', 10)]
    trump_suit = 'Hearts'
    legal_cards = human_player.hand[:2]
    chosen_card = human_player.play_card(cards_on_table, trump_suit, legal_cards)
    assert chosen_card == legal_cards[0]
    assert chosen_card not in human_player.hand