import pytest
import sys

sys.path.append("..")
from batak import Batak, Card, BotPlayer
from unittest.mock import patch


@pytest.fixture
def players():
    hands = [
        [
            Card("Hearts", 14),
            Card("Hearts", 13),
            Card("Spades", 10),
            Card("Clubs", 9),
            Card("Diamonds", 2),
        ],
        [
            Card("Spades", 14),
            Card("Spades", 13),
            Card("Hearts", 12),
            Card("Clubs", 3),
            Card("Diamonds", 3),
        ],
        [
            Card("Diamonds", 14),
            Card("Clubs", 13),
            Card("Hearts", 11),
            Card("Hearts", 10),
            Card("Spades", 3),
        ],
        [
            Card("Clubs", 14),
            Card("Spades", 9),
            Card("Diamonds", 10),
            Card("Hearts", 9),
            Card("Clubs", 2),
        ],
    ]
    player_list = []
    for i, hand in enumerate(hands):
        player_list.append(
            BotPlayer(name=f"Player {i + 1}", hand=hand.copy())
        )
    return player_list


def test_is_play_legal_leading_card(players):
    game = Batak(players)
    game.trump = "Spades"
    game.is_trump_enabled = False
    game.cards_on_table = []
    game.current_player_index = 0
    card = Card("Hearts", 14)
    assert game.is_play_legal(card) is True


def test_is_play_legal_following_same_suit(players):
    game = Batak(players)
    game.trump = "Diamonds"
    game.is_trump_enabled = True
    game.cards_on_table = [Card("Hearts", 10), Card("Hearts", 9)]
    game.current_player_index = 0
    card = Card("Hearts", 14)
    assert game.is_play_legal(card) is True
    assert game.is_play_legal(Card("Hearts", 13)) is True
    assert game.is_play_legal(Card("Hearts", 8)) is False
    assert game.is_play_legal(Card("Diamonds", 2)) is False
    


def test_is_play_legal_trump_required(players):
    game = Batak(players)
    game.trump = "Spades"
    game.cards_on_table = [Card("Clubs", 10)]
    game.current_player_index = 1
    players[1].hand = [Card("Spades", 13), Card("Hearts", 2)]
    card = Card("Hearts", 2)
    # Must play trump
    assert game.is_play_legal(card) is False

def test_is_play_legal_trump_required2(players):
    game = Batak(players)
    game.trump = "Spades"
    game.cards_on_table = [Card("Clubs", 10)]
    game.current_player_index = 1
    players[1].hand = [Card("Spades", 13), Card("Hearts", 2)]
    card = Card("Spades", 13)
    # Must play trump
    assert game.is_play_legal(card) is True

def test_is_play_legal_trump_not_yet_enabled(players):
    game = Batak(players)
    game.trump = "Hearts"
    game.is_trump_enabled = False
    game.cards_on_table = []
    game.current_player_index = 0
    players[0].hand = [Card("Hearts", 14), Card("Spades", 10)]
    card = Card("Hearts", 14)
    # Cannot lead with trump if not enabled and other suits are available
    assert game.is_play_legal(card) is False


@patch("batak.BotPlayer.bid", side_effect=[7, 5, 6, 4])
@patch("batak.BotPlayer.choose_trump", return_value="Spades")
def test_bidding_and_trump_selection(mock_trump, mock_bids, players):
    game = Batak(players)
    game.bidding()
    assert game.trump == "Spades"
    assert game.current_player_index == 0  # Player 1 wins with bid 7


def test_determine_winning_card_trump_wins(players):
    game = Batak(players)
    game.trump = "Hearts"
    game.cards_on_table = [
        Card("Clubs", 2),
        Card("Hearts", 10),
        Card("Spades", 12),
        Card("Hearts", 9),
    ]
    game.roundwinnerindexoffset = 0
    game.determine_winning_card()
    assert game.roundwinner == 1  # Index of 'Hearts', 10


def test_determine_winning_card_no_trump(players):
    game = Batak(players)
    game.trump = "Diamonds"
    game.cards_on_table = [
        Card("Hearts", 10),
        Card("Hearts", 9),
        Card("Hearts", 13),
        Card("Clubs", 11),
    ]
    game.roundwinnerindexoffset = 3
    game.determine_winning_card()
    assert game.roundwinner == 1  # 'Hearts', 13 wins


@patch("batak.BotPlayer.play_card", side_effect=lambda table, trump, legal: legal[0])
def test_full_round_simulation(mock_play_card, players):
    game = Batak(players)
    game.trump = "Hearts"
    game.is_trump_enabled = False
    game.current_player_index = 0
    game.gameround()
    # After round, round winner should have increased score
    assert any(p.score == 1 for p in players)
    assert len(game.cards_on_table) == 4

def test_no_need_to_rise_if_trump_on_table(players):
    game = Batak(players)
    game.trump = "Spades"
    game.is_trump_enabled = True # Enabled because someone played one
    
    # SETUP:
    # Lead is Hearts 10.
    # Player 2 (or whoever) has ALREADY played a Spade (Trump) on the table.
    game.cards_on_table = [Card("Hearts", 10), Card("Spades", 2)] 
    
    # Current Player (Player 1)
    game.current_player_index = 0
    # Player 1 has a low Heart and a high Heart (Ace/14)
    players[0].hand = [Card("Hearts", 14), Card("Hearts", 5), Card("Clubs", 2)]
    
    # THE TEST:
    # Logic: Normally, played card (H5) < Table (H10), so you MUST play H14.
    # But because Spades (Trump) is on the table, H14 cannot win anyway.
    # So playing H5 should be LEGAL.
    
    card_to_play = Card("Hearts", 5)
    
    # If this fails, your code is still enforcing "Must Rise" even when trumped
    assert game.is_play_legal(card_to_play) is True

def test_must_over_trump_if_possible(players):
    game = Batak(players)
    game.trump = "Spades"
    
    # SETUP:
    # Lead is Diamonds.
    # Someone else has already cut with Spades 9.
    game.cards_on_table = [Card("Diamonds", 10), Card("Spades", 9)]
    
    game.current_player_index = 0
    # Player 1 is void in Diamonds (Lead), so must play Trump.
    # They have Spades 5 (lower than table) and Spades 12 (higher).
    players[0].hand = [Card("Spades", 5), Card("Spades", 12), Card("Hearts", 10)]
    
    # SCENARIO 1: Player tries to play Spades 5 (Under-trump)
    # This should be ILLEGAL because they have S12 which beats S9.
    assert game.is_play_legal(Card("Spades", 5)) is False
    
    # SCENARIO 2: Player plays Spades 12 (Over-trump)
    # This is correct.
    assert game.is_play_legal(Card("Spades", 12)) is True

def test_can_under_trump_if_cannot_beat(players):
    game = Batak(players)
    game.trump = "Spades"
    
    # SETUP:
    # Lead is Diamonds. Table has a High Trump (Spades Ace/14).
    game.cards_on_table = [Card("Diamonds", 10), Card("Spades", 14)]
    
    game.current_player_index = 0
    # Player 1 is void in Diamonds.
    # They only have small trumps (S2, S3). Neither can beat S14.
    players[0].hand = [Card("Spades", 2), Card("Spades", 3), Card("Hearts", 10)]
    
    # In this case, since they can't win, they can play any trump.
    assert game.is_play_legal(Card("Spades", 2)) is True
