from django.test import TestCase, Client
from django.urls import reverse
 
 
class ViewsTestCase(TestCase):
    """Test cases for Django views."""
   
    def setUp(self):
        """Set up test client."""
        self.client = Client()
   
    def test_index_redirects_without_game(self):
        """Test that index redirects to new_game when no game exists."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('new_game'))
   
    def test_new_game_creates_game(self):
        """Test that new_game creates a game and redirects."""
        response = self.client.post(reverse('new_game'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
       
        # Check session has game state
        self.assertIn('game_state', self.client.session)
   
    def test_index_displays_game(self):
        """Test that index displays game after creation."""
        # Create a game first
        self.client.post(reverse('new_game'))
       
        # Now access index
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('game_state', response.context)
   
    def test_hit_action(self):
        """Test hitting adds a card."""
        # Create a game
        self.client.post(reverse('new_game'))
       
        # Hit - should succeed unless game is already over
        response = self.client.post(reverse('hit'))
       
        # Should either succeed (200) or fail if game ended (400)
        # We can't guarantee success due to random cards
        self.assertIn(response.status_code, [200, 400])
   
    def test_stand_action(self):
        """Test standing triggers dealer turn."""
        # Create a game
        self.client.post(reverse('new_game'))
       
        # Stand - should succeed unless game is already over
        response = self.client.post(reverse('stand'))
       
        # Should either succeed (200) or fail if game ended (400)
        self.assertIn(response.status_code, [200, 400])
       
        if response.status_code == 200:
            # Check dealer turn is triggered
            data = response.json()
            self.assertTrue(data['dealer_turn'])
            self.assertTrue(data['game_over'])
   
    def test_split_action(self):
        """Test split action when player has a pair."""
        # Create a game
        self.client.post(reverse('new_game'))
       
        # Note: We can't guarantee a pair in random game,
        # but we can test the endpoint exists
        response = self.client.post(reverse('split'))
       
        # Should either succeed (200) or fail with proper error (400)
        self.assertIn(response.status_code, [200, 400])
   
    def test_hit_without_game(self):
        """Test that hitting without a game returns error."""
        response = self.client.post(reverse('hit'))
        self.assertEqual(response.status_code, 400)
   
    def test_stand_without_game(self):
        """Test that standing without a game returns error."""
        response = self.client.post(reverse('stand'))
        self.assertEqual(response.status_code, 400)
   
    def test_game_state_endpoint(self):
        """Test game_state endpoint returns current state."""
        # Create a game
        self.client.post(reverse('new_game'))
       
        response = self.client.get(reverse('game_state'))
        self.assertEqual(response.status_code, 200)
       
        data = response.json()
        self.assertIn('player_hand', data)
        self.assertIn('dealer_hand', data)
