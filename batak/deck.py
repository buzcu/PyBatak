from typing import List
import random
from batak.card import Card

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.build()

    def build(self) -> None:
        """Initialize a standard 52-card deck."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = range(2, 15)  # 2-10, J=11, Q=12, K=13, A=14
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self) -> None:
        """Randomize the order of cards."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int = 1) -> List[Card]:
        """Remove and return `num_cards` from the deck."""
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck!")
        dealt_cards = []
        for i in range(num_cards):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"Deck({len(self)} cards remaining)"