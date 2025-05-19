class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        names = {11: "J", 12: "Q", 13: "K", 14: "A"}
        return f"{names.get(self.rank, self.rank)} of {self.suit}"
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    def get_value(self):
        return self.rank
    def get_suit(self):
        return self.suit
    def __hash__(self):
        return hash((self.suit, self.rank))
    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)
    def __gt__(self, other):
        return (self.suit, self.rank) > (other.suit, other.rank)  
