from .card import Card
from .constants import BLACKJACK
 
 
class Hand:
    """Represents a hand of cards in Blackjack."""
   
    def __init__(self):
        self.cards = []
   
    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)
   
    def get_value(self):
        """
        Calculate the value of the hand, properly handling Aces.
        Aces count as 11 unless that would cause a bust, then they count as 1.
        """
        value = 0
        aces = 0
       
        for card in self.cards:
            if card.is_ace():
                aces += 1
                value += 11
            else:
                value += card.value
       
        # Adjust for Aces if we're over 21
        while value > BLACKJACK and aces > 0:
            value -= 10  # Convert an Ace from 11 to 1
            aces -= 1
       
        return value
   
    def is_bust(self):
        """Check if the hand is over 21."""
        return self.get_value() > BLACKJACK
   
    def is_blackjack(self):
        """Check if the hand is a natural Blackjack (21 with first two cards)."""
        return len(self.cards) == 2 and self.get_value() == BLACKJACK
   
    def can_split(self):
        """Check if the hand can be split (two cards of the same rank)."""
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
   
    def __str__(self):
        cards_str = ', '.join(str(card) for card in self.cards)
        return f"Hand: [{cards_str}] (Value: {self.get_value()})"
   
    def __len__(self):
        return len(self.cards)
   
    def to_dict(self):
        """Convert hand to dictionary for JSON serialization."""
        return {
            'cards': [card.to_dict() for card in self.cards],
            'value': self.get_value(),
            'is_bust': self.is_bust(),
            'is_blackjack': self.is_blackjack()
        }
   
    @classmethod
    def from_dict(cls, data):
        """Create a Hand instance from a dictionary."""
        hand = cls()
        hand.cards = [Card.from_dict(card_data) for card_data in data['cards']]
        return hand