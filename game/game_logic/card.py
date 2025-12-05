from .constants import CARD_VALUES, FACE_CARD_NAMES


class Card:
    """Represents a single playing card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALUES[rank]
   
    def __str__(self):
        rank = self.rank
        if (self.rank in FACE_CARD_NAMES):
            rank = FACE_CARD_NAMES[self.rank]
        return f"{rank} of {self.suit}"
   
    def __repr__(self):
        return f"Card('{self.suit}', '{self.rank}')"
   
    def is_ace(self):
        """Check if the card is an Ace."""
        return self.rank == 'A'
   
    def to_dict(self):
        """Convert card to dictionary for JSON serialization."""
        return {
            'suit': self.suit,
            'rank': self.rank,
            'value': self.value
        }
   
    @classmethod
    def from_dict(cls, data):
        """Create a Card instance from a dictionary."""
        return cls(data['suit'], data['rank'])