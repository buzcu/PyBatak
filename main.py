import sys
sys.path.append("/batak")

from batak.game import Game
from batak.player import Player
from batak.deck import Deck
import random

def run_game():
    deck = Deck()
    deck.shuffle()

    players = [Player(f'Player {i+1}', is_bot=True, hand=deck.deal(13)) for i in range(4)]
    random.shuffle(players)  # Optional

    game = Game(players)
    game.bidding()

    for _ in range(13):
        game.gameround()

    print("\nFinal Scores:")
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name}: {player.score}")

if __name__ == '__main__':
    run_game()