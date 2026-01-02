"""Module defining the Player class for the Batak card game."""
from typing import List, Optional
from .card import Card
from .play_strategies import PlayStrategies, RuleBasedPlayStrategies


class Player:
    """Class representing a player in the Batak game."""
    def __init__(self, name, is_bot=False, hand: Optional[List[Card]] = None):
        self.name = name
        self.is_bot = is_bot
        self.hand = hand
        self.score = 0

    def print_hand(self):
        """Print the player's hand."""
        print(f"{self.name}'s hand: " + ", ".join(str(card) for card in self.hand))

    def bid(self) -> int:
        """Get the player's bid for the round."""

    def choose_trump(self):
        """Choose the trump suit for the round."""

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        """Play a card from the player's hand."""


class HumanPlayer(Player):
    """Class representing a human player in the Batak game."""
    def __init__(self, name, hand: Optional[List[Card]] = None):
        super().__init__(name, is_bot=False, hand=hand)
        self.print_hand()

    def bid(self) -> int:
        """Get the player's bid for the round."""
        return int(input(f"{self.name}, enter your bid: "))

    def choose_trump(self):
        """Choose the trump suit for the round."""
        trump_suit = input(
            f"{self.name}, choose a trump suit (Hearts, Diamonds, Clubs, Spades): "
        )
        while trump_suit not in Card.VALID_SUITS:
            trump_suit = input("Invalid suit. Choose again: ")
        return trump_suit

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        """Play a card from the player's hand."""
        print(f"Cards on table: {', '.join(map(str, cards_on_table))}")
        print(f"Legal cards: {', '.join(map(str, legal_cards))}")
        try:
            choice = int(
                input(
                    f"{self.name}, choose a card index to play (0-{len(legal_cards) - 1}): "
                )
            )
            while choice < 0 or choice >= len(legal_cards):
                choice = int(
                    input(
                        f"Invalid index. {self.name}, choose a " +
                        "card index to play (0-{len(legal_cards) - 1}): "
                    )
                )
        except ValueError:
            print("Invalid input. Playing the first legal card by default.")
            choice = 0
        chosen = legal_cards[choice]
        self.hand.remove(chosen)
        return chosen

class BotPlayer(Player):
    """Class representing a bot player in the Batak game."""
    def __init__(self, name, hand: Optional[List[Card]] = None,
                 strategy: Optional[PlayStrategies] = RuleBasedPlayStrategies(),
                 position: Optional[str] = None):
        super().__init__(name, is_bot=True, hand=hand)
        self.strategy = strategy
        self.position = position

    def bid(self) -> int:
        """Get the bot's bid for the round."""
        return self.strategy.bid(self.hand)

    def choose_trump(self):
        """Choose the trump suit for the round."""
        return self.strategy.choose_trump(self.hand)

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        """Play a card from the player's hand."""
        chosen_card = self.strategy.play_card(cards_on_table, trump_suit, legal_cards)
        self.hand.remove(chosen_card)
        return chosen_card
