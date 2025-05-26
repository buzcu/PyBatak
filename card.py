class Card:
    """Represents a standard playing card with a suit and rank."""

    VALID_SUITS = {'Hearts', 'Diamonds', 'Clubs', 'Spades'}
    FACE_CARD_NAMES = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, suit, rank):
        """Initialize a card with a suit and rank.
        
        Args:
            suit: One of 'Hearts', 'Diamonds', 'Clubs', 'Spades'.
            rank: Integer between 2 and 14 (Ace-high).
        
        Raises:
            ValueError: If suit or rank is invalid.
        """
        if rank < 2 or rank > 14:
            raise ValueError("Rank must be between 2 and 14")
        if suit not in self.VALID_SUITS:
            raise ValueError(f"Invalid suit. Must be one of {self.VALID_SUITS}")
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        """Return a human-readable string representation of the card."""
        return f"{self.FACE_CARD_NAMES.get(self.rank, self.rank)} of {self.suit}"


    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return  self.rank > other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __ge__(self, other):
        return  self.rank >= other.rank

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.suit == other.suit and self.rank == other.rank
        
    def __hash__(self):
        return hash((self.suit, self.rank))

    def get_value(self):
        """Return the rank of the card."""
        return self.rank

    def get_suit(self):
        """Return the suit of the card."""
        return self.suit