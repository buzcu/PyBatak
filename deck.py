import random
from card import Card

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = list(range(2, 15))

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self, num_players=4):
        return [self.cards[i::num_players] for i in range(num_players)]
