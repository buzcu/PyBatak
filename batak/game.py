"""Module implementing the core game logic for Batak."""
from typing import List
from .card import Card
from .player import Player

class Game:
    """Class representing a Batak game."""
    def __init__(self, players: list[Player]):
        self.players = players
        self.trump = None
        self.is_trump_enabled = False
        self.cards_on_table = []
        self.current_player_index = 0
        self.roundwinner = None
        self.roundwinnerindexoffset = 0

    def players_cards_in_suit(self, player: Player, suit: str) -> List[Card]:
        """Return a list of cards in `player`'s hand that match `suit`."""
        return [card for card in player.hand if card.suit == suit]

    def _can_lead_card(self, player: Player, card: Card) -> bool:
        """Return True if `card` can be led when table is empty.

        Preserves original behaviour: non-trump can always be led; trump
        can only be led when trump is enabled or player only has trump cards.
        """
        if card.suit != self.trump:
            return True
        # card is trump
        if not self.is_trump_enabled:
            if len(player.hand) == len(self.players_cards_in_suit(player, self.trump)):
                return True
            return False
        return True

    def _can_follow_same_suit_with_trump_enabled(self,
                                                 player: Player,
                                                 card: Card,
                                                 trump_on_table) -> bool:
        # If player plays a non-trump of the leading suit, it's allowed.
        if card.suit != self.trump:
            return True

        # Card is trump: compare ranks against highest trump on table
        highest_trump_on_table = max(trump_on_table)
        if card.rank > highest_trump_on_table.rank:
            return True

        # Player may play a lower trump only if they have an even higher trump
        player_trumps = [hc for hc in player.hand if hc.suit == self.trump]
        if player_trumps and highest_trump_on_table.rank < max(player_trumps).rank:
            return True
        return False

    def _can_follow_same_suit(self, player: Player, card: Card, leading_suit: str) -> bool:
        """Return True if `card` is legal when following the leading suit.

        Implements the existing logic that considers whether trump is enabled
        and whether trumps are on the table. Uses card ordering (rank) as before.
        """
        # If trumps are enabled and there is at least one trump on the table,
        # special rules apply.
        trump_on_table = [c for c in self.cards_on_table if c.suit == self.trump]
        if self.is_trump_enabled and any(trump_on_table):
            return self._can_follow_same_suit_with_trump_enabled(player, card, trump_on_table)
        # Regular same-suit following rules (no special trump-on-table case)
        highest_on_table_same = max(
            filter(lambda c: c.suit == leading_suit, self.cards_on_table)
        )
        if card.rank > highest_on_table_same.rank:
            return True

        highest_in_hand_same = max(filter(lambda c: c.suit == leading_suit, player.hand))
        if highest_in_hand_same.rank < highest_on_table_same.rank:
            return True

        return False

    def _can_follow_different_suit(self, player: Player, card: Card, leading_suit: str) -> bool:
        """Return True if `card` is legal when it does NOT match the leading suit."""
        if len(self.players_cards_in_suit(player, leading_suit)) == 0:
            if card.suit == self.trump:
                return True
            if len(self.players_cards_in_suit(player, self.trump)) == 0:
                return True
            return False
        return False

    def is_play_legal(self, card: Card):
        """Check if playing the given card is legal according to game rules."""
        player = self.players[self.current_player_index]

        # Leading play
        if len(self.cards_on_table) == 0:
            return self._can_lead_card(player, card)

        leading_suit = self.cards_on_table[0].suit
        if card.suit == leading_suit:
            return self._can_follow_same_suit(player, card, leading_suit)

        return self._can_follow_different_suit(player, card, leading_suit)

    def bidding(self):
        """Conduct the bidding phase to determine trump suit and starting player."""
        bids = [player.bid() for player in self.players]
        max_bid_index = bids.index(max(bids))

        self.trump = self.players[max_bid_index].choose_trump()
        print(
            "Trump: " + self.trump + " by player: " + self.players[max_bid_index].name
        )
        self.current_player_index = max_bid_index  # bid winner starts first

    def determine_winning_card(self):
        """Determine the winning card and the round winner."""
        trump_cards = [card for card in self.cards_on_table if card.suit == self.trump]
        if trump_cards:
            winningcard = max(trump_cards)
        else:
            same_suit_cards = [
                card
                for card in self.cards_on_table
                if card.suit == self.cards_on_table[0].suit
            ]
            winningcard = max(same_suit_cards)
        self.roundwinner = (
            self.cards_on_table.index(winningcard) + self.roundwinnerindexoffset
        ) % 4

    def gameround(self):
        """Conduct a single round of the game."""
        self.cards_on_table.clear()
        self.roundwinner = None
        self.roundwinnerindexoffset = self.current_player_index
        player = self.players[self.current_player_index]
        for _ in range(4):
            print("\nCurrent player: " + player.name)
            print("Cards on table: " + str([str(card) for card in self.cards_on_table]))
            print("Player hand: " + str([str(card) for card in player.hand]))
            print("players card options are as follows:")
            legal_cards = [card for card in player.hand if self.is_play_legal(card)]

            if len(legal_cards) == 0:
                print(" !!! ERROR: No legal cards available !!!")
                print("Player cards are: " + str([str(card) for card in player.hand]))
                print("Cards on table: " + str([str(card) for card in self.cards_on_table]))
                print("Trump is: " + str(self.trump))
                print("Current player is: " + str(player.name))
                return
            print("Cards: " + str([str(card) for card in legal_cards]))
            played_card = player.play_card(self.cards_on_table, self.trump, legal_cards)
            if played_card is None:
                print(" !!! ERROR: No card played !!!")
                return
            if played_card not in legal_cards:
                print(" !!! ERROR: Card not legal !!!")
                return
            if played_card.suit == self.trump:
                self.is_trump_enabled = True

            print("" + player.name + " played: " + str(played_card))
            self.cards_on_table.append(played_card)
            self.current_player_index = (self.current_player_index + 1) % 4
            player = self.players[self.current_player_index]

        self.determine_winning_card()

        print("Round winner: " + self.players[self.roundwinner].name)
        self.players[self.roundwinner].score += 1
        self.current_player_index = self.roundwinner
