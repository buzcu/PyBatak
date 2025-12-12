"""
Docstring for main.py 
This is the entry point for the Batak game in console mode.
"""
import random
from batak.game import Game
from batak.player import HumanPlayer, BotPlayer
from batak.deck import Deck
from batak import RandomPlayStrategies, HighCardPlayStrategies

def run_bot_game():
    """
    Runs a console-based Batak game with 4 bots.
    """
    deck = Deck()
    deck.shuffle()

    players = []
    players.append(BotPlayer("Rule Based Bot Player", hand=deck.deal(13)))
    players.append(BotPlayer("Rule Based Bot Player 2", hand=deck.deal(13)))
    players.append(BotPlayer("Random Bot Player", hand=deck.deal(13),
                             strategy=RandomPlayStrategies()))
    players.append(BotPlayer("highest card Bot Player", hand=deck.deal(13),
                             strategy=HighCardPlayStrategies()))
    random.shuffle(players)  # Optional

    game = Game(players)
    game.bidding()

    for _ in range(13):
        game.gameround()

    print("\nFinal Scores:")
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name}: {player.score}")

def run_human_game():
    """
    Runs a console-based Batak game with 4 players (3 bots and 1 human).
    """
    deck = Deck()
    deck.shuffle()

    players = []
    players.append(BotPlayer("Rule Based Bot Player", hand=deck.deal(13)))
    players.append(HumanPlayer("Human", hand=deck.deal(13)))
    players.append(BotPlayer("Random Bot Player", hand=deck.deal(13),
                             strategy=RandomPlayStrategies()))
    players.append(BotPlayer("highest card Bot Player", hand=deck.deal(13),
                             strategy=HighCardPlayStrategies()))
    random.shuffle(players)  # Optional

    game = Game(players)
    game.bidding()

    for _ in range(13):
        game.gameround()

    print("\nFinal Scores:")
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name}: {player.score}")
if __name__ == "__main__":
    print("Welcome to Batak Game!")
    choice = input("Do you want to play as a human? (y/n): ").strip().lower()
    if choice == 'y':
        run_human_game()
    run_bot_game()
