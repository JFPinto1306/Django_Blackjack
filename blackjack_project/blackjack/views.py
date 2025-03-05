from django.shortcuts import render
from .models import Game, Deck, Card
from .game_logic import Blackjack

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer

# Create your views here.

class GameView(APIView):
    def get(self, request):
        game = Game.objects.last()
        if not game:
            return Response({"message": "No game found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def post(self, request):
        game = Game.objects.last()
        if not game:
            game = Game.objects.create()
            game.save()
        else:
            # Reset the game state instead of deleting it
            game.status = "STARTED"
            game.player_hand.clear()
            game.dealer_hand.clear()
            game.player_score = 0
            game.dealer_score = 0
            game.winner = None
            game.save()
            
        blackjack_game = Blackjack()
        blackjack_game.start_game()

        # Fetch the updated game from the database to ensure it reflects changes
        game.refresh_from_db()

        serializer = GameSerializer(game)

        return Response(serializer.data) 

class PlayerHitView(APIView):
    def post(self, request):
        game = Game.objects.last()
        if not game:
            return Response({"message": "No game in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Implement the "hit" logic
        blackjack_game = Blackjack()
        new_card = blackjack_game.hit(game.player_hand)  # Method to deal one card
        
        game.player_score = blackjack_game.calculate_score(game.player_hand)
        
        # Save the new card in the database
        game.save()

        
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

class DealerHitView(APIView):
    def post(self, request):
        game = Game.objects.last()
        if not game:
            return Response({"message": "No game in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Implement the "hit" logic
        blackjack_game = Blackjack()
        new_card = blackjack_game.hit(game.dealer_hand)  # Method to deal one card
        
        game.dealer_score = blackjack_game.calculate_score(game.dealer_hand)
        
        # Save the new card in the database
        game.save()

        
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)


class WinnerView(APIView):
    def post(self, request):
        # Initialize the Blackjack game logic
        blackjack_game = Blackjack()
        
        # Call the internal game logic to determine the winner
        winner = blackjack_game.get_winner()  # This indirectly calls get_winner
        
        # Fetch the updated game state
        game = blackjack_game.game
        serializer = GameSerializer(game)
        
        # Return the game state, winner, and message
        return Response({
            "game_state": serializer.data,
            "winner": winner,
            "message": f"{winner} wins!"
        }, status=status.HTTP_200_OK)