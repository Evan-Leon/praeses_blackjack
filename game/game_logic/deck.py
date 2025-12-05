import random
from .card import Card
from .constants import SUITS, RANKS
 
 
class Deck:
    """Represents a deck of 52 playing cards."""
   
    def __init__(self):
        self.cards = []
        self.reset()
   
    def reset(self):
        """Create a fresh deck of 52 cards."""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
   
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
   
    def deal(self):
        """Deal one card from the top of the deck."""
        if not self.cards:
            raise ValueError("Cannot deal from an empty deck")
        return self.cards.pop()
   
    def cards_remaining(self):
        """Return the number of cards left in the deck."""
        return len(self.cards)
   
    def __len__(self):
        return len(self.cards)
   
    def __str__(self):
        return f"Deck with {len(self.cards)} cards"
   
    def to_dict(self):
        """Convert deck to dictionary for JSON serialization."""
        return {
            'cards': [card.to_dict() for card in self.cards]
        }
   
    @classmethod
    def from_dict(cls, data):
        """Create a Deck instance from a dictionary."""
        deck = cls()
        deck.cards = [Card.from_dict(card_data) for card_data in data['cards']]
        return deck