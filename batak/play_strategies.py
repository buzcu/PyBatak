"""Module containing play strategies for Batak bots."""
from typing import List
import random
from .card import Card

class PlayStrategies:
    """Base class for play strategies for Batak bots."""
    def play_card(self, cards_on_table: List[Card],
                  trump_suit: str, legal_cards: List[Card]) -> Card:
        """Play a card from the player's hand."""

    def bid(self, hand:List[Card]) -> int:
        """Make a bid for the round."""

    def choose_trump(self, hand:List[Card]) -> str:
        """Choose the trump suit for the round."""

class RandomPlayStrategies(PlayStrategies):
    """Random play strategies for Batak bots."""

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        return random.choice(legal_cards)

    def bid(self, hand) -> int:
        return min(random.randint(5, 12),
                   random.randint(5, 12),
                   random.randint(5, 12))

    def choose_trump(self, hand) -> str:
        return random.choice(list(Card.VALID_SUITS))

class HighCardPlayStrategies(PlayStrategies):
    """play the highest card rank strategy for Batak bots."""

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        return max(legal_cards, key=lambda c: c.rank)

    def bid(self, hand) -> int:
        return min(random.randint(5, 12),
                   random.randint(5, 12),
                   random.randint(5, 12))

    def choose_trump(self, hand) -> str:
        return random.choice(list(Card.VALID_SUITS))

class RuleBasedPlayStrategies(PlayStrategies):
    """Rule-based play strategies for Batak bots."""

    def play_card(self, cards_on_table, trump_suit, legal_cards):
        return self._rule_based_play(cards_on_table, trump_suit, legal_cards)

    def bid(self, hand) -> int:
        return self.simple_bid_logic(hand)

    def number_of_cards_in_suit(self, suit: str, hand:List[Card]) -> int:
        """Return the number of cards in the player's hand of a given suit."""
        return len([card for card in hand if card.suit == suit])

    def simple_bid_logic(self, hand) -> int:
        """Simple logic for bot to determine its bid based on high cards."""
        high_cards = [card for card in hand if card.rank >= 11]
        return min(13, max(5, len(high_cards) // 2 + 1))

    def choose_trump(self, hand:List[Card])-> str:
        """Choose the trump suit for the round."""
        return self.simple_trump_logic(hand)

    def simple_trump_logic(self, hand:List[Card])-> str:
        """Simple logic to choose a trump suit based on the player's hand."""
        suits = {card.suit for card in hand}
        if len(suits) == 1:
            return suits.pop()
        # Choose the suit with the most cards in `hand`.
        suit_numbers = {}
        for s in suits:
            suit_numbers[s] = self.number_of_cards_in_suit(s, hand)
        return max(suit_numbers, key=suit_numbers.get)

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
        """Rule-based logic in a regular round without trump played yet."""
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
