from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import Game, Deck, Card
from .serializers import GameSerializer
from .game_logic import Blackjack

# Create your views here.
class GameHandler(viewsets.ViewSet):
    # Get a game, either the latest one or by specific game ID
    def retrieve(self, request, pk=None):
        if pk:
            # Get the specific game by game_id (pk)
            game = get_object_or_404(Game, id=pk)
        else:
            # Get the last game if no game_id is provided
            game = Game.objects.last()
            if not game:
                return Response({"message": "No game found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game)
        return Response(serializer.data)

    # Create a new game
    def create(self, request):
        blackjack_game = Blackjack()
        blackjack_game.start_game()

        serializer = GameSerializer(blackjack_game.game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['post'])
    def hit(self, request, pk):
        if pk:
            # Get the specific game by game_id (pk)
            game = get_object_or_404(Game, id=pk)
            blackjack_game = Blackjack(game_id=pk)

            player_score = blackjack_game.hit(blackjack_game.player_hand)
            dealer_score = blackjack_game.calculate_score(blackjack_game.dealer_hand)

            # Update game with scores
            game.player_score = player_score
            game.dealer_score = dealer_score
            game.save()

            serializer = GameSerializer(game)
            return Response(serializer.data)
        else:
            return Response({"message": "Game ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def winner(self, request, pk):
        if pk:
            # Get the specific game by game_id (pk)
            blackjack_game = Blackjack(game_id=pk)

            blackjack_game.get_winner()
            
            game = get_object_or_404(Game, id=pk)

            
            serializer = GameSerializer(game)
            return Response(serializer.data)
        else:
            return Response({"message": "Game ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        