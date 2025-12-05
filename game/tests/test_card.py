from django.test import TestCase
from game.game_logic.card import Card
 
 
class CardTestCase(TestCase):
    """Test cases for the Card class."""
   
    def test_card_creation(self):
        """Test creating a card with suit and rank."""
        card = Card('Hearts', 'A')
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.value, 11)
   
    def test_card_values(self):
        """Test that cards have correct values."""
        self.assertEqual(Card('Hearts', '2').value, 2)
        self.assertEqual(Card('Hearts', '10').value, 10)
        self.assertEqual(Card('Hearts', 'J').value, 10)
        self.assertEqual(Card('Hearts', 'Q').value, 10)
        self.assertEqual(Card('Hearts', 'K').value, 10)
        self.assertEqual(Card('Hearts', 'A').value, 11)
   
    def test_is_ace(self):
        """Test ace detection."""
        ace = Card('Hearts', 'A')
        king = Card('Spades', 'K')
        self.assertTrue(ace.is_ace())
        self.assertFalse(king.is_ace())
   
    def test_card_string_representation(self):
        """Test card string representation."""
        jack = Card('Diamonds', 'J')
        self.assertEqual(str(jack), 'Jack of Diamonds')
        queen = Card('Clubs', 'Q')
        self.assertEqual(str(queen), 'Queen of Clubs')
        king = Card('Spades', 'K')
        self.assertEqual(str(king), 'King of Spades')
        ace = Card('Hearts', 'A')
        self.assertEqual(str(ace), 'Ace of Hearts')
        number = Card('Hearts', '2')
        self.assertEqual(str(number), '2 of Hearts')
   
    def test_card_serialization(self):
        """Test card to_dict and from_dict methods."""
        card = Card('Diamonds', 'K')
        card_dict = card.to_dict()
       
        self.assertEqual(card_dict['suit'], 'Diamonds')
        self.assertEqual(card_dict['rank'], 'K')
        self.assertEqual(card_dict['value'], 10)
       
        # Test deserialization
        restored_card = Card.from_dict(card_dict)
        self.assertEqual(restored_card.suit, 'Diamonds')
        self.assertEqual(restored_card.rank, 'K')
        self.assertEqual(restored_card.value, 10)