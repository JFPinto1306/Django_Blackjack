from rest_framework import serializers
from .models import Card, Game


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'suit', 'value']
        
        
class GameSerializer(serializers.ModelSerializer):
    player_hand = CardSerializer(many=True)
    dealer_hand = CardSerializer(many=True)
    player_score = serializers.IntegerField()
    dealer_score = serializers.IntegerField()
    
    class Meta:
        model = Game
        fields = ['id', 'status', 'player_hand', 'dealer_hand', 'player_score', 'dealer_score', 'winner']