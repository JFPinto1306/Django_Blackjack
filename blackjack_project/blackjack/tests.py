from django.test import TestCase
from .models import *

class CardModelTest(TestCase):
    def setUp(self):
        self.card = Card.objects.create(value='A', suit='Hearts')

    def test_card_str(self):
        self.assertEqual(str(self.card), "A of Hearts")

    def test_card_value(self):
        # Testing Ace value when current score is 0
        self.assertEqual(self.card.get_card_value(), 11)

        # Testing Ace value when current score would bust
        self.assertEqual(self.card.get_card_value(15), 1)

class GameModelTest(TestCase):
    def setUp(self):
        self.deck = Deck.objects.create()
        self.deck.start_deck()
        self.game = Game.objects.create(status='STARTED')

    def test_game_status(self):
        self.assertEqual(self.game.status, 'STARTED')

    def test_player_hand(self):
        self.assertEqual(self.game.player_hand.count(), 0)  # Player has 0 card
        self.assertEqual(self.game.dealer_hand.count(), 0)  # Dealer has 0 card
        
    def test_add_card(self):
        # Add a card to the player's hand
        self.deck.deal_card(self.game.player_hand)
        self.assertEqual(self.game.player_hand.count(), 1)

