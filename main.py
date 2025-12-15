"""
Docstring for main.py 
This is the entry point for the Batak game in console mode.
"""
import random
from batak.game import Batak
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

    game = Batak(players)
    game.bidding()

    for _ in range(13):
        game.gameround()
    final_scores = {}
    print("\nFinal Scores:")
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name}: {player.score}")
        final_scores[player.name] = player.score
    return final_scores

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

    game = Batak(players)
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
    elif choice == 'a':
        final_score_array = []
        num_games = int(input("Enter number of bot games to simulate: "))
        for _ in range(num_games):
            final_score_array.append(run_bot_game())
        
        aggregated_scores = {}
        for score_dict in final_score_array:    
            for name, score in score_dict.items():
                if name in aggregated_scores:
                    aggregated_scores[name] += score
                else:
                    aggregated_scores[name] = score
        print("\nAggregated Scores after {} games:".format(num_games))
        for name, score in aggregated_scores.items():
            print(f"{name}: {score}")
    else:
        run_bot_game()
