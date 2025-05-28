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
    
    game = Game(players)
    for i in range(4):
        game.register_bids(players[i].bid())
    game.bidding_results()
    trump = game.get_trump()

    for _ in range(13):
        player_index = game.start_round()
        for i in range(4):
            game.register_played_card(players[(player_index+i)%4].play_card(game.get_cards_on_table(), game.get_trump(), game.get_legal_cards()))
        game.finalize_round()

    print("\nFinal Scores:")
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name}: {player.score}")

if __name__ == '__main__':
    run_game()