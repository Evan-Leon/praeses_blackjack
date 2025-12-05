from .deck import Deck
from .hand import Hand
from .constants import BLACKJACK, DEALER_STAND_VALUE
 
 
class BlackjackGame:
    """Manages the core Blackjack game logic and rules."""
   
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.result = None
        self.dealer_turn = False
        self.split_hand = None
        self.active_hand = 'main' # 'main' or 'split'
   
    def start_new_game(self):
        """Initialize a new game with shuffled deck and dealt cards."""
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.result = None
        self.dealer_turn = False
        self.split_hand = None
        self.active_hand = 'main'
       
        # Deal initial cards (player, dealer, player, dealer)
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
       
        # Check for immediate blackjack
        if self.player_hand.is_blackjack():
            self.dealer_turn = True
            if self.dealer_hand.is_blackjack():
                self.game_over = True
                self.result = 'push'
            else:
                self.game_over = True
                self.result = 'player_blackjack'
        elif self.dealer_hand.is_blackjack():
            self.dealer_turn = True
            self.game_over = True
            self.result = 'dealer_blackjack'
   
    def player_hit(self):
        """Player takes another card."""
        if self.game_over or self.dealer_turn:
            return False

        current_hand = self.split_hand if self.active_hand == 'split' else self.player_hand
        current_hand.add_card(self.deck.deal())
       
        if current_hand.is_bust():
            if self.active_hand == 'main' and self.split_hand:
                self.active_hand = 'split'
                return True

            self.dealer_turn = True
            self._dealer_play()
            return True
       
        return True
   
    def player_stand(self):
        """Player chooses to stand, dealer's turn begins."""
        if self.game_over or self.dealer_turn:
            return False

        if self.active_hand == 'main' and self.split_hand:
            self.active_hand = 'split'
            return True
       
        self.dealer_turn = True
        self._dealer_play()
        return True

    def player_split(self):
        """Split the player's hand into two hands."""
        if self.game_over or self.dealer_turn or self.split_hand:
            return False

        if not self.player_hand.can_split():
            return False
       
        # Create split hand with second card
        self.split_hand = Hand()
        self.split_hand.add_card(self.player_hand.cards.pop())
       
        # Deal new cards to both hands
        self.player_hand.add_card(self.deck.deal())
        self.split_hand.add_card(self.deck.deal())

        return True
   
    def _dealer_play(self):
        """Execute dealer's turn according to Blackjack rules."""
        # Dealer must hit until reaching 17 or higher
        while self.dealer_hand.get_value() < DEALER_STAND_VALUE:
            self.dealer_hand.add_card(self.deck.deal())
       
        # Determine winner
        self._determine_winner()
   
    def _determine_winner(self):
        """Determine the game outcome."""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
       
        # Handle split hands
        if self.split_hand:
            split_value = self.split_hand.get_value()
            main_result = self._compare_hands(player_value, dealer_value, self.player_hand.is_bust())
            split_result = self._compare_hands(split_value, dealer_value, self.split_hand.is_bust())
           
            # Check for wins, losses, and pushes
            main_wins = 'wins' in main_result or 'dealer_bust' in main_result
            split_wins = 'wins' in split_result or 'dealer_bust' in split_result
            main_loses = 'player_bust' in main_result or 'dealer_wins' in main_result
            split_loses = 'player_bust' in split_result or 'dealer_wins' in split_result
            main_push = 'push' in main_result
            split_push = 'push' in split_result
            
            # Determine overall result based on all combinations
            if main_wins and split_wins:
                self.result = 'both_win'
            elif main_loses and split_loses:
                self.result = 'both_lose'
            elif main_push and split_push:
                self.result = 'both_push'
            elif main_wins and split_push:
                self.result = 'win_and_push'
            elif main_push and split_wins:
                self.result = 'win_and_push'
            elif main_loses and split_push:
                self.result = 'lose_and_push'
            elif main_push and split_loses:
                self.result = 'lose_and_push'
            else:
                # One wins, one loses
                self.result = 'win_and_lose'
        else:
            self.result = self._compare_hands(player_value, dealer_value, self.player_hand.is_bust())
       
        self.game_over = True
   
    def _compare_hands(self, player_value, dealer_value, player_bust):
        """Compare a single hand against dealer."""
        if player_bust:
            return 'player_bust'
        elif self.dealer_hand.is_bust():
            return 'dealer_bust'
        elif player_value > dealer_value:
            return 'player_wins'
        elif dealer_value > player_value:
            return 'dealer_wins'
        else:
            return 'push'
   
    def get_game_state(self):
        """Return the current game state as a dictionary."""
        return {
            'player_hand': self.player_hand.to_dict(),
            'split_hand': self.split_hand.to_dict() if self.split_hand else None,
            'active_hand': self.active_hand,
            'dealer_hand': self.dealer_hand.to_dict(),
            'dealer_showing': self._get_dealer_showing(),
            'game_over': self.game_over,
            'dealer_turn': self.dealer_turn,
            'result': self.result,
            'result_message': self._get_result_message(),
            'can_split': self.player_hand.can_split() and not self.split_hand and not self.dealer_turn
        }
   
    def _get_dealer_showing(self):
        """Get dealer's visible card information (only first card before dealer's turn)."""
        if not self.dealer_turn and len(self.dealer_hand.cards) > 0:
            first_card = self.dealer_hand.cards[0]
            return {
                'card': first_card.to_dict(),
                'hidden_cards': len(self.dealer_hand.cards) - 1
            }
        return None
   
    def _get_result_message(self):
        """Convert result code to a human-readable message."""
        messages = {
            'player_blackjack': 'Blackjack! You win!',
            'dealer_blackjack': 'Dealer has Blackjack. You lose.',
            'player_bust': 'Bust! You lose.',
            'dealer_bust': 'Dealer busts! You win!',
            'player_wins': 'You win!',
            'both_win': 'You won both hands!',
            'both_lose': 'You lost both hands.',
            'both_push': 'Both hands push (tie).',
            'win_and_lose': 'Split result: One hand won, one hand lost.',
            'win_and_push': 'Split result: One hand won, one hand pushed.',
            'lose_and_push': 'Split result: One hand lost, one hand pushed.',
            'dealer_wins': 'Dealer wins.',
            'push': "It's a push (tie)."
        }
        return messages.get(self.result, '')
   
    def to_dict(self):
        """Serialize the entire game state for session storage."""
        return {
            'deck': self.deck.to_dict(),
            'player_hand': self.player_hand.to_dict(),
            'split_hand': self.split_hand.to_dict() if self.split_hand else None,
            'active_hand': self.active_hand,
            'dealer_hand': self.dealer_hand.to_dict(),
            'game_over': self.game_over,
            'dealer_turn': self.dealer_turn,
            'result': self.result
        }
   
    @classmethod
    def from_dict(cls, data):
        """Restore a game from serialized state."""
        game = cls()
        game.deck = Deck.from_dict(data['deck'])
        game.player_hand = Hand.from_dict(data['player_hand'])
        game.split_hand = Hand.from_dict(data['split_hand']) if data.get('split_hand') else None
        game.active_hand = data.get('active_hand', 'main')
        game.dealer_hand = Hand.from_dict(data['dealer_hand'])
        game.game_over = data['game_over']
        game.dealer_turn = data['dealer_turn']
        game.result = data['result']
        return game