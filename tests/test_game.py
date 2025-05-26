import pytest
import sys
sys.path.append("..")
from game import Game
from player import Player
from card import Card
from unittest.mock import patch


@pytest.fixture
def players():
    hands = [
        [Card('Hearts', 14), Card('Hearts', 13), Card('Spades', 10), Card('Clubs', 9), Card('Diamonds', 2)],
        [Card('Spades', 14), Card('Spades', 13), Card('Hearts', 12), Card('Clubs', 3), Card('Diamonds', 3)],
        [Card('Diamonds', 14), Card('Clubs', 13), Card('Hearts', 11), Card('Hearts', 10), Card('Spades', 3)],
        [Card('Clubs', 14), Card('Spades', 9), Card('Diamonds', 10), Card('Hearts', 9), Card('Clubs', 2)]
    ]
    player_list = []
    for i, hand in enumerate(hands):
        player_list.append(Player(name=f"Player {i+1}", is_bot=True, hand=hand.copy()))
    return player_list


def test_is_play_legal_leading_card(players):
    game = Game(players)
    game.trump = 'Spades'
    game.is_trump_enabled = False
    game.cards_on_table = []
    game.current_player_index = 0
    card = Card('Hearts', 14)
    assert game.is_play_legal(card) is True


def test_is_play_legal_following_same_suit(players):
    game = Game(players)
    game.trump = 'Diamonds'
    game.cards_on_table = [Card('Hearts', 10), Card('Hearts', 9)]
    game.current_player_index = 0
    card = Card('Hearts', 14)
    assert game.is_play_legal(card) is True


def test_is_play_legal_trump_required(players):
    game = Game(players)
    game.trump = 'Spades'
    game.cards_on_table = [Card('Clubs', 10)]
    game.current_player_index = 1
    players[1].hand = [Card('Spades', 13), Card('Hearts', 2)]
    card = Card('Hearts', 2)
    # Must play trump
    assert game.is_play_legal(card) is False


@patch('player.Player.bid', side_effect=[7, 5, 6, 4])
@patch('player.Player.choose_trump', return_value='Spades')
def test_bidding_and_trump_selection(mock_trump, mock_bids, players):
    game = Game(players)
    game.bidding()
    assert game.trump == 'Spades'
    assert game.current_player_index == 0  # Player 1 wins with bid 7


def test_determine_winning_card_trump_wins(players):
    game = Game(players)
    game.trump = 'Hearts'
    game.cards_on_table = [
        Card('Clubs', 2),
        Card('Hearts', 10),
        Card('Spades', 12),
        Card('Hearts', 9)
    ]
    game.roundwinnerindexoffset = 0
    game.determine_winning_card()
    assert game.roundwinner == 1  # Index of 'Hearts', 10


def test_determine_winning_card_no_trump(players):
    game = Game(players)
    game.trump = 'Diamonds'
    game.cards_on_table = [
        Card('Hearts', 10),
        Card('Hearts', 9),
        Card('Hearts', 13),
        Card('Clubs', 11)
    ]
    game.roundwinnerindexoffset = 3
    game.determine_winning_card()
    assert game.roundwinner == 1  # 'Hearts', 13 wins


@patch('player.Player.play_card', side_effect=lambda table, trump, legal: legal[0])
def test_full_round_simulation(mock_play_card, players):
    game = Game(players)
    game.trump = 'Hearts'
    game.is_trump_enabled = False
    game.current_player_index = 0
    game.gameround()
    # After round, round winner should have increased score
    assert any(p.score == 1 for p in players)
    assert len(game.cards_on_table) == 4