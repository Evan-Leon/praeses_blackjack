from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .game_logic.game import BlackjackGame
import json
 
 
def get_or_create_game(request):
    """Retrieve or create a game from session data."""
    game_data = request.session.get('game_state')
   
    if game_data:
        try:
            return BlackjackGame.from_dict(game_data)
        except Exception:
            game = BlackjackGame()
            game.start_new_game()
            save_game(request, game)
            return game
   
    return None
 
 
def save_game(request, game):
    """Save game state to session."""
    request.session['game_state'] = game.to_dict()
    request.session.modified = True
 
@require_http_methods(["GET"])
def index(request):
    """Main game view."""
    game = get_or_create_game(request)
    if not game:
        # No active game, redirect to new game
        return redirect('new_game')

    game_state = game.get_game_state()

    context = {
        'game_state': game_state,
    }
   
    return render(request, 'game.html', context)
 
 
@require_http_methods(["POST"])
def new_game(request):
    """Start a new game."""
    game = BlackjackGame()
    game.start_new_game()
    save_game(request, game)
   
    return redirect('index')
 
 
@require_http_methods(["POST"])
def hit(request):
    """Player hits (takes another card)."""
    game = get_or_create_game(request)
   
    if not game:
        return JsonResponse({'error': 'No active game'}, status=400)
   
    success = game.player_hit()
   
    if not success:
        return JsonResponse({'error': 'Cannot hit'}, status=400)
   
    save_game(request, game)

    return JsonResponse(game.get_game_state())
 
 
@require_http_methods(["POST"])
def stand(request):
    """Player stands (ends their turn)."""
    game = get_or_create_game(request)
   
    if not game:
        return JsonResponse({'error': 'No active game'}, status=400)
   
    success = game.player_stand()
   
    if not success:
        return JsonResponse({'error': 'Cannot stand'}, status=400)
   
    save_game(request, game)
   
    return JsonResponse(game.get_game_state())

@require_http_methods(["POST"])
def split(request):
    """Player splits their hand."""
    game = get_or_create_game(request)

    if not game:
        return JsonResponse({'error': 'No active game'}, status=400)

    success = game.player_split()

    if not success:
        return JsonResponse({'error': 'Cannot split'}, status=400)

    save_game(request, game)

    return JsonResponse(game.get_game_state())
 
 
@require_http_methods(["GET"])
def game_state(request):
    """Get current game state as JSON (for AJAX updates)."""
    game = get_or_create_game(request)
   
    if not game:
        return JsonResponse({'error': 'No active game'}, status=400)
   
    return JsonResponse(game.get_game_state())