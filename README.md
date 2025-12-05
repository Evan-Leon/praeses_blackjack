# Praeses Blackjack
 
## **Developer:** Evan Leon

**LiveLink:** [Praeses Blackjack](https://praeses-blackjack-5101a346b252.herokuapp.com/)
---
 
## Thank You
 
Thank you for the opportunity to interview with Praeses and for reviewing this technical assessment. I enjoyed building this Blackjack application and demonstrating my approach to Django web development.
 
---
 
## Overview
 
This is a web-based Blackjack game built with Django and Python. The application implements core Blackjack gameplay with proper game logic, clean architecture, and comprehensive testing.

### Core Features
 
- **Standard Blackjack gameplay** 
- **Dealer logic** 
- **Win condition detection** 
- **Ace handling** 
- **Session-based game state** 
- **Clean, modular code structure**
 
### Bonus Features
 
- **Hand Splitting** - Players can split pairs into two separate hands and play each independently
  - Available when dealt two cards of the same rank
  - Each hand is played sequentially
  - Results are calculated separately for each hand with clear messaging
- **Testing** - Test game, deck, hand and view (instructions below)
 
---

## Setup and Installation
 
### Prerequisites
 
- Python 3.8 or higher
- pip (Python package manager)
 
### Installation Steps
 
1. **Clone or extract the project**
   ```bash
   cd praeses_blackjack
   ```
 
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```
 
3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
 
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
 
5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```
 
6. **Start the development server**
   ```bash
   python manage.py runserver
   ```
 
7. **Open your browser**
  
   Navigate to: `http://127.0.0.1:8000/`
 
---
 
## Running Tests
 
The project includes a comprehensive test suite covering all game logic and views.
 
```bash
# Run all tests
python manage.py test
 
# Run tests with verbose output
python manage.py test --verbosity=2
 
# Run specific test file
python manage.py test game.tests.test_game
 
# Run specific test class
python manage.py test game.tests.test_game.BlackjackGameTestCase
 
# Run specific test method
python manage.py test game.tests.test_game.BlackjackGameTestCase.test_player_hit
```
 
All tests should pass successfully.
 
---
 
## How to Play
 
1. **Start a New Game** - Click "New Game" to begin
2. **Your Turn** - You'll see your two cards and one of the dealer's cards
3. **Make Your Move:**
   - **Hit** - Take another card
   - **Stand** - End your turn and let the dealer play
   - **Split** (if available) - Split pairs into two separate hands
4. **Dealer's Turn** - The dealer will automatically play according to standard rules
5. **See Results** - The winner is determined and displayed
6. **Play Again** - Click "New Game" to start another round
 
---

## Contact
 
Evan Leon 
Evan.Leon.J@gmail.com
Github: Evan-Leon
