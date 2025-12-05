from django.test import TestCase
from game.game_logic.hand import Hand
from game.game_logic.card import Card

class HandTestCase(TestCase):
    """Test cases for the Hand class."""
   
    def test_empty_hand(self):
        """Test creating an empty hand."""
        hand = Hand()
        self.assertEqual(len(hand.cards), 0)
        self.assertEqual(hand.get_value(), 0)
   
    def test_add_card(self):
        """Test adding cards to a hand."""
        hand = Hand()
        card = Card('Hearts', 'K')
        hand.add_card(card)
       
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(hand.get_value(), 10)
   
    def test_hand_value_simple(self):
        """Test hand value calculation without aces."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'K'))
        hand.add_card(Card('Spades', '7'))
       
        self.assertEqual(hand.get_value(), 17)
   
    def test_hand_value_with_ace_as_11(self):
        """Test ace counted as 11."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', '9'))
       
        self.assertEqual(hand.get_value(), 20)
   
    def test_hand_value_with_ace_as_1(self):
        """Test ace counted as 1 to avoid bust."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', 'K'))
        hand.add_card(Card('Diamonds', '5'))
       
        # Ace should be 1, not 11 (1 + 10 + 5 = 16)
        self.assertEqual(hand.get_value(), 16)
   
    def test_hand_value_multiple_aces(self):
        """Test multiple aces in hand."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', 'A'))
        hand.add_card(Card('Diamonds', '9'))
       
        # Should be 1 + 1 + 9 = 11 (or 1 + 11 + 9 = 21)
        self.assertEqual(hand.get_value(), 21)
   
    def test_is_bust(self):
        """Test bust detection."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'K'))
        hand.add_card(Card('Spades', 'Q'))
        hand.add_card(Card('Diamonds', '5'))
       
        self.assertTrue(hand.is_bust())
   
    def test_not_bust(self):
        """Test non-bust hand."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'K'))
        hand.add_card(Card('Spades', '10'))
       
        self.assertFalse(hand.is_bust())
   
    def test_blackjack_detection(self):
        """Test blackjack (21 with 2 cards) detection."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', 'K'))
       
        self.assertTrue(hand.is_blackjack())
        self.assertEqual(hand.get_value(), 21)
   
    def test_not_blackjack_three_cards(self):
        """Test that 21 with 3 cards is not blackjack."""
        hand = Hand()
        hand.add_card(Card('Hearts', '7'))
        hand.add_card(Card('Spades', '7'))
        hand.add_card(Card('Diamonds', '7'))
       
        self.assertFalse(hand.is_blackjack())
        self.assertEqual(hand.get_value(), 21)
   
    def test_can_split_same_rank(self):
        """Test splitting with same rank cards."""
        hand = Hand()
        hand.add_card(Card('Hearts', '8'))
        hand.add_card(Card('Spades', '8'))
       
        self.assertTrue(hand.can_split())
   
    def test_can_split_face_cards(self):
        """Test splitting with face cards."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'K'))
        hand.add_card(Card('Spades', 'K'))
       
        self.assertTrue(hand.can_split())
   
    def test_cannot_split_different_ranks(self):
        """Test that different ranks cannot be split."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'K'))
        hand.add_card(Card('Spades', 'Q'))
       
        self.assertFalse(hand.can_split())
   
    def test_cannot_split_three_cards(self):
        """Test that hand with 3 cards cannot split."""
        hand = Hand()
        hand.add_card(Card('Hearts', '8'))
        hand.add_card(Card('Spades', '8'))
        hand.add_card(Card('Diamonds', '8'))
       
        self.assertFalse(hand.can_split())
   
    def test_hand_serialization(self):
        """Test hand serialization and deserialization."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', 'K'))
       
        hand_dict = hand.to_dict()
       
        self.assertEqual(len(hand_dict['cards']), 2)
        self.assertEqual(hand_dict['value'], 21)
        self.assertTrue(hand_dict['is_blackjack'])
       
        # Test deserialization
        restored_hand = Hand.from_dict(hand_dict)
        self.assertEqual(len(restored_hand.cards), 2)
        self.assertEqual(restored_hand.get_value(), 21)
 