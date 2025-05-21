from deck import Deck
from player import Player
from card import Card
import random

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

class BatakGame:
    def __init__(self):
        self.players = [Player(f"Player {i+1}", is_bot=True) for i in range(4)]
        self.trump_suit = None
        self.deck = Deck()

    def deal_cards(self):
        hands = self.deck.deal()
        for player, hand in zip(self.players, hands):
            player.hand = hand

    def run_bidding(self):
        highest_bid = 0
        bidder = None
        for player in self.players:
            bid = player.make_bid(highest_bid)
            if bid > highest_bid:
                highest_bid = bid
                bidder = player
        self.trump_suit = random.choice(SUITS)
        bidder.bid = highest_bid
        return bidder

    def play_trick(self, lead_index):
        table = []
        lead_suit = None
        for i in range(4):
            player = self.players[(lead_index + i) % 4]
            card = player.play_card(lead_suit, self.trump_suit)
            if i == 0:
                lead_suit = card.suit
            table.append((player, card))

        winning_card = max(
            table,
            key=lambda x: (x[1].suit == self.trump_suit, x[1].suit == lead_suit, x[1].rank)
        )
        winner = winning_card[0]
        winner.tricks_won += 1
        return self.players.index(winner)

    def play_round(self):
        self.deal_cards()
        self.run_bidding()
        lead = 0
        for _ in range(13):
            lead = self.play_trick(lead)

    def run(self):
        self.play_round()
        for p in self.players:
            print(f"{p.name} won {p.tricks_won} tricks.")
