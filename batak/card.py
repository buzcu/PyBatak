from dataclasses import dataclass, field


@dataclass(order=True, frozen=True)
class Card:
    sort_index: int = field(init=False, repr=False)
    suit: str
    rank: int

    VALID_SUITS = {"Hearts", "Diamonds", "Clubs", "Spades"}
    FACE_CARD_NAMES = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __post_init__(self):
        # Validation logic
        if self.rank < 2 or self.rank > 14:
            raise ValueError("Rank must be between 2 and 14")
        if self.suit not in self.VALID_SUITS:
            raise ValueError(f"Invalid suit. Must be one of {self.VALID_SUITS}")

        # We set a sort_index because we want to sort by rank, ignoring suit
        # frozen=True makes the card immutable (can't change a 5 to a King later)
        object.__setattr__(self, "sort_index", self.rank)

    def __str__(self):
        return f"{self.FACE_CARD_NAMES.get(self.rank, self.rank)} of {self.suit}"
