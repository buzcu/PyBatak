from mcts import MCTS, GameState
from card import Card

class Player:
    def __init__(self, name, is_bot=False):
        self.name = name
        self.is_bot = is_bot
        self.hand = []
        self.tricks_won = 0
        self.bid = 0

    def number_of_cards_in_suit(self, suit):
        """Return the number of cards in the player's hand of a given suit."""
        return len([card for card in self.hand if card.suit == suit])

    def make_bid(self, bids_so_far):
        if self.is_bot:
            return self.simple_bid_logic(bids_so_far)
        else:
            return int(input(f"{self.name}, enter your bid: "))

    def simple_bid_logic(self, bids_so_far):
        high_cards = [card for card in self.hand if card.rank >= 11]
        return min(13, max(5, len(high_cards) // 2 + 1))

    def play_card(self, current_suit, trump_suit):
        print(f"{self.name}'s hand: {[str(card) for card in self.hand]}")
        #if self.is_bot:
        #    state = GameState(self.hand, [], current_suit, trump_suit)
        #    mcts = MCTS(state, iterations=100)
        #    chosen = mcts.search()
        #else:
        valid_cards = [card for card in self.hand if card.suit == current_suit] or self.hand
        while True:
            try:
                choice = int(input(f"{self.name}, choose a card index to play (0-{len(valid_cards)-1}): "))
                chosen = valid_cards[choice]
                break
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")
        self.hand.remove(chosen)
        return chosen