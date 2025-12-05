from django.test import TestCase
from game.game_logic.deck import Deck
from game.game_logic.card import Card
 
 
class DeckTestCase(TestCase):
    """Test cases for the Deck class."""
   
    def test_deck_initialization(self):
        """Test that a new deck has 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
   
    def test_deck_has_all_cards(self):
        """Test that deck contains all suits and ranks."""
        deck = Deck()
        suits = set()
        ranks = set()
       
        for card in deck.cards:
            suits.add(card.suit)
            ranks.add(card.rank)
       
        self.assertEqual(len(suits), 4)
        self.assertEqual(len(ranks), 13)
   
    def test_deck_shuffle(self):
        """Test that shuffle changes card order."""
        deck1 = Deck()
        deck2 = Deck()
       
        # Get original order
        original_order = [str(card) for card in deck1.cards]
       
        # Shuffle deck2
        deck2.shuffle()
        shuffled_order = [str(card) for card in deck2.cards]
       
        # Orders should be different (with very high probability)
        self.assertNotEqual(original_order, shuffled_order)
   
    def test_deal_card(self):
        """Test dealing a card from the deck."""
        deck = Deck()
        initial_count = len(deck.cards)
       
        card = deck.deal()
       
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)
   
    def test_deal_all_cards(self):
        """Test dealing all cards from deck."""
        deck = Deck()
       
        for _ in range(52):
            deck.deal()
       
        self.assertEqual(len(deck.cards), 0)
   
    def test_deal_from_empty_deck(self):
        """Test that dealing from empty deck raises error."""
        deck = Deck()
       
        # Deal all cards
        for _ in range(52):
            deck.deal()
       
        # Try to deal from empty deck
        with self.assertRaises(ValueError):
            deck.deal()
   
    def test_cards_remaining(self):
        """Test cards_remaining method."""
        deck = Deck()
        self.assertEqual(deck.cards_remaining(), 52)
       
        deck.deal()
        self.assertEqual(deck.cards_remaining(), 51)
   
    def test_deck_reset(self):
        """Test resetting the deck."""
        deck = Deck()
        deck.deal()
        deck.deal()
       
        deck.reset()
       
        self.assertEqual(len(deck.cards), 52)
   
    def test_deck_serialization(self):
        """Test deck serialization and deserialization."""
        deck = Deck()
        deck.shuffle()
        deck.deal()  # Remove one card
       
        deck_dict = deck.to_dict()
        self.assertEqual(len(deck_dict['cards']), 51)
       
        # Test deserialization
        restored_deck = Deck.from_dict(deck_dict)
        self.assertEqual(len(restored_deck.cards), 51)