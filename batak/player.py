"""Module defining the Player class for the Batak card game."""
from typing import List, Optional
from .card import Card


class Player:
    """Class representing a player in the Batak game."""
    def __init__(self, name, is_bot=False, hand: Optional[List[Card]] = None):
        self.name = name
        self.is_bot = is_bot
        self.hand = hand
        self.score = 0

    def number_of_cards_in_suit(self, suit: str) -> int:
        """Return the number of cards in the player's hand of a given suit."""
        return len([card for card in self.hand if card.suit == suit])

    def bid(self) -> int:
        """Get the player's bid for the round."""
        if self.is_bot:
            return self.simple_bid_logic()
        return int(input(f"{self.name}, enter your bid: "))

    def simple_bid_logic(self) -> int:
        """Simple logic for bot to determine its bid based on high cards."""
        high_cards = [card for card in self.hand if card.rank >= 11]
        return min(13, max(5, len(high_cards) // 2 + 1))

    def choose_trump(self):
        """Choose the trump suit for the round."""
        if self.is_bot:
            return self.simple_trump_logic()
        trump_suit = input(
            f"{self.name}, choose a trump suit (Hearts, Diamonds, Clubs, Spades): "
        )
        while trump_suit not in Card.VALID_SUITS:
            trump_suit = input("Invalid suit. Choose again: ")
        return trump_suit

    def simple_trump_logic(self):
        """Simple logic to choose a trump suit based on the player's hand."""
        suits = {card.suit for card in self.hand}
        if len(suits) == 1:
            return suits.pop()
        return max(suits, key=self.number_of_cards_in_suit)

    def _rule_based_trump_round(
        self, cards_on_table: List[Card], trump_suit: str, legal_cards: List[Card]
    ) -> Card:
        """Rule-based logic for playing in a trump round."""
        same_suit_cards = [
            card for card in legal_cards if card.suit == cards_on_table[0].suit
        ]
        if len(same_suit_cards) == 0:
            chosen = min(legal_cards)
        else:
            trump_cards = [card for card in legal_cards if card.suit == trump_suit]

            if len(trump_cards) == 1:
                chosen = trump_cards[0]
            else:
                if max(trump_cards) > max(cards_on_table):
                    chosen = max(trump_cards)
                else:
                    chosen = min(trump_cards)
        return chosen

    def _rule_based_regular_round_without_trump(
        self, cards_on_table: List[Card], trump_suit: str, legal_cards: List[Card]
    ) -> Card:
        """Rule-based logic for playing in a regular round without trump played yet."""
        same_suit_cards = [
            card for card in legal_cards if card.suit == cards_on_table[0].suit
        ]
        if len(same_suit_cards) == 0:
            if len(legal_cards) == 1:
                chosen = legal_cards[0]
            else:
                trump_cards = [card for card in legal_cards if card.suit == trump_suit]
                if trump_cards:
                    chosen = min(trump_cards)
                else:
                    chosen = min(legal_cards)

        else:
            if len(same_suit_cards) == 1:
                chosen = same_suit_cards[0]
            else:
                if max(same_suit_cards) > max(cards_on_table):
                    chosen = max(same_suit_cards)
                else:
                    chosen = min(same_suit_cards)
        return chosen

    def _rule_based_regular_round_with_trump(
        self, cards_on_table: List[Card], trump_suit: str, legal_cards: List[Card]
    ) -> Card:
        """Rule-based logic for playing in a regular round with trump played."""
        same_suit_cards = [
            card for card in legal_cards if card.suit == cards_on_table[0].suit
        ]
        if len(same_suit_cards) > 0:
            chosen = min(same_suit_cards)
        else:
            trump_cards = [card for card in legal_cards if card.suit == trump_suit]
            if trump_cards:
                if len(trump_cards) == 1:
                    chosen = trump_cards[0]
                else:
                    if max(trump_cards) > max(cards_on_table):
                        chosen = max(trump_cards)
                    else:
                        chosen = min(trump_cards)
            else:
                chosen = min(legal_cards)
        return chosen

    def _rule_based_regular_round(
        self, cards_on_table: List[Card], trump_suit: str, legal_cards: List[Card]
    ) -> Card:
        """Rule-based logic for playing in a regular round."""
        if not any(card.suit == trump_suit for card in cards_on_table):
            chosen = self._rule_based_regular_round_without_trump(
                cards_on_table, trump_suit, legal_cards
            )
        else:
            chosen = self._rule_based_regular_round_with_trump(
                cards_on_table, trump_suit, legal_cards
            )
        return chosen

    def _rule_based_play(
        self, cards_on_table: List[Card], trump_suit: str, legal_cards: List[Card]
    ) -> Card:
        """Rule-based logic for bot to play a card."""
        if len(cards_on_table) == 0:
            chosen = min(legal_cards)
            return chosen
        is_it_trump_round = cards_on_table[0].suit == trump_suit
        if not is_it_trump_round:
            chosen = self._rule_based_regular_round(
                cards_on_table, trump_suit, legal_cards
            )
        else:
            chosen = self._rule_based_trump_round(
                cards_on_table, trump_suit, legal_cards
            )
        return chosen

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        """Play a card from the player's hand."""
        if self.is_bot:
            chosen = self._rule_based_play(cards_on_table, trump_suit, legal_cards)
        else:
            print(f"Legal cards: {', '.join(map(str, legal_cards))}")
            print(f"Cards on table: {', '.join(map(str, cards_on_table))}")
            choice = int(
                input(
                    f"{self.name}, choose a card index to play (0-{len(legal_cards) - 1}): "
                )
            )
            chosen = legal_cards[choice]
        self.hand.remove(chosen)
        return chosen
