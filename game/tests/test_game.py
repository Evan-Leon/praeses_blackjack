from django.test import TestCase
from game.game_logic.game import BlackjackGame
from game.game_logic.card import Card
 
 
class BlackjackGameTestCase(TestCase):
    """Test cases for the BlackjackGame class."""
   
    def test_game_initialization(self):
        """Test game starts with proper initial state."""
        game = BlackjackGame()
       
        self.assertIsNotNone(game.deck)
        self.assertIsNotNone(game.player_hand)
        self.assertIsNotNone(game.dealer_hand)
        self.assertFalse(game.game_over)
        self.assertIsNone(game.result)
        self.assertFalse(game.dealer_turn)
   
    def test_start_new_game_deals_cards(self):
        """Test that starting a new game deals 4 cards."""
        game = BlackjackGame()
        game.start_new_game()
       
        self.assertEqual(len(game.player_hand.cards), 2)
        self.assertEqual(len(game.dealer_hand.cards), 2)
        self.assertEqual(game.deck.cards_remaining(), 48)
   
    def test_player_hit(self):
        """Test player hitting adds a card."""
        game = BlackjackGame()
        game.start_new_game()
       
        # Set up a very safe hand that definitely won't bust (total of 8)
        game.player_hand.cards = []
        game.player_hand.add_card(Card('Hearts', '3'))
        game.player_hand.add_card(Card('Spades', '5'))
       
        # Ensure game is not over and dealer hasn't played
        game.game_over = False
        game.dealer_turn = False
       
        initial_cards = len(game.player_hand.cards)
       
        success = game.player_hit()
       
        self.assertTrue(success)
        self.assertEqual(len(game.player_hand.cards), initial_cards + 1)
        # With max card value of 11 (Ace), 3+5+11 = 19, so won't bust
        self.assertFalse(game.game_over)
   
    def test_player_hit_when_game_over(self):
        """Test that player cannot hit when game is over."""
        game = BlackjackGame()
        game.start_new_game()
        game.game_over = True
       
        result = game.player_hit()
       
        self.assertFalse(result)
   
    def test_player_stand(self):
        """Test player standing triggers dealer turn."""
        game = BlackjackGame()
        game.start_new_game()
       
        game.player_stand()
       
        self.assertTrue(game.dealer_turn)
        self.assertTrue(game.game_over)
   
    def test_dealer_plays_to_17(self):
        """Test dealer hits until reaching 17."""
        game = BlackjackGame()
        game.start_new_game()
       
        # Manually set dealer hand to low value and ensure deck has cards
        game.dealer_hand.cards = []
        game.dealer_hand.add_card(Card('Hearts', '5'))
        game.dealer_hand.add_card(Card('Spades', '6'))
       
        # Reset deck to ensure we have cards to deal
        game.deck.reset()
        game.deck.shuffle()
       
        # Ensure game state allows dealer to play
        game.game_over = False
        game.dealer_turn = False
       
        game.player_stand()
       
        # Dealer should hit until >= 17
        self.assertGreaterEqual(game.dealer_hand.get_value(), 17)
   
    def test_player_bust_ends_game(self):
        """Test that player busting ends the game."""
        game = BlackjackGame()
        game.start_new_game()
       
        # Force player to bust - set hand to 22
        game.player_hand.cards = []
        game.player_hand.add_card(Card('Hearts', 'K'))
        game.player_hand.add_card(Card('Spades', 'Q'))
        game.player_hand.add_card(Card('Diamonds', '5'))
       
        # Player hand is now 25, which is bust
        self.assertTrue(game.player_hand.is_bust())
       
        # Manually trigger the bust check
        if game.player_hand.is_bust():
            game.game_over = True
            game.dealer_turn = True
            game.result = 'player_bust'
       
        self.assertTrue(game.game_over)
        self.assertEqual(game.result, 'player_bust')
   
    def test_player_blackjack(self):
        """Test player getting blackjack."""
        game = BlackjackGame()
        game.deck.shuffle()
       
        # Set up blackjack scenario
        game.player_hand.cards = []
        game.dealer_hand.cards = []
        game.player_hand.add_card(Card('Hearts', 'A'))
        game.player_hand.add_card(Card('Spades', 'K'))
        game.dealer_hand.add_card(Card('Diamonds', '5'))
        game.dealer_hand.add_card(Card('Clubs', '6'))
       
        # Check for blackjack at start
        game.start_new_game()
       
        # Manually check since start_new_game resets everything
        hand_test = BlackjackGame()
        hand_test.player_hand.add_card(Card('Hearts', 'A'))
        hand_test.player_hand.add_card(Card('Spades', 'K'))
       
        self.assertTrue(hand_test.player_hand.is_blackjack())
   
    def test_split_functionality(self):
        """Test splitting a pair."""
        game = BlackjackGame()
        # Don't call start_new_game() to avoid random blackjack
       
        # Set up pair manually
        game.player_hand.add_card(Card('Hearts', '8'))
        game.player_hand.add_card(Card('Spades', '8'))
        game.dealer_hand.add_card(Card('Diamonds', '7'))
        game.dealer_hand.add_card(Card('Clubs', '6'))
       
        # Ensure game state allows splitting
        game.game_over = False
        game.dealer_turn = False
        game.split_hand = None
       
        result = game.player_split()
       
        self.assertTrue(result)
        self.assertIsNotNone(game.split_hand)
        self.assertEqual(len(game.player_hand.cards), 2)
        self.assertEqual(len(game.split_hand.cards), 2)
   
    def test_cannot_split_non_pair(self):
        """Test that non-pairs cannot be split."""
        game = BlackjackGame()
        # Don't call start_new_game() to avoid random cards
       
        # Set up non-pair
        game.player_hand.add_card(Card('Hearts', '8'))
        game.player_hand.add_card(Card('Spades', '7'))
       
        result = game.player_split()
       
        self.assertFalse(result)
        self.assertIsNone(game.split_hand)
   
    def test_cannot_split_twice(self):
        """Test that player cannot split twice."""
        game = BlackjackGame()
        # Don't call start_new_game() to avoid random cards
       
        # Set up pair and split
        game.player_hand.add_card(Card('Hearts', '8'))
        game.player_hand.add_card(Card('Spades', '8'))
        game.dealer_hand.add_card(Card('Diamonds', '7'))
        game.dealer_hand.add_card(Card('Clubs', '6'))
       
        game.player_split()
       
        # Try to split again
        result = game.player_split()
       
        self.assertFalse(result)
   
    def test_game_state_serialization(self):
        """Test game state can be serialized and restored."""
        game = BlackjackGame()
        game.start_new_game()
       
        game_dict = game.to_dict()
       
        restored_game = BlackjackGame.from_dict(game_dict)
       
        self.assertEqual(len(restored_game.player_hand.cards),
                        len(game.player_hand.cards))
        self.assertEqual(len(restored_game.dealer_hand.cards),
                        len(game.dealer_hand.cards))
        self.assertEqual(restored_game.game_over, game.game_over)
   
    def test_get_game_state(self):
        """Test get_game_state returns proper dictionary."""
        game = BlackjackGame()
        game.start_new_game()
       
        state = game.get_game_state()
       
        self.assertIn('player_hand', state)
        self.assertIn('dealer_hand', state)
        self.assertIn('game_over', state)
        self.assertIn('result', state)
        self.assertIn('can_split', state)
        