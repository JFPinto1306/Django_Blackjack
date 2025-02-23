from django.test import TestCase
from .models import *
from .game_logic import Blackjack
from django.db.models import QuerySet


class CardModelTest(TestCase):
    def setUp(self):
        self.card = Card.objects.create(value='A', suit='Hearts')

    def test_ace_card_str(self):
        self.assertEqual(str(self.card), "A of Hearts")

    def test_ace_card_value(self):
        # Testing Ace value when current score is 0
        self.assertEqual(self.card.get_card_value(0), 11)

        # Testing Ace value when current score would bust
        self.assertEqual(self.card.get_card_value(15), 1)
        #print(f"Card: {self.card}, Value: {self.card.get_card_value(15)}")
    
    def test_other_card(self):
        self.card = Card.objects.create(value='5', suit='Hearts')
        # Testing Ace value when current score is 0
        self.assertEqual(self.card.get_card_value(0), 5)
        #print(f"Card: {self.card}, Value: {self.card.get_card_value(15)}")
        
        
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
        
    def test_deck_initialization(self):
        self.assertEqual(self.deck.cards.count(), 52, "Deck should have 52 cards after initialization")
    
    def taken_card_not_in_deck(self):
        # Take a card from the deck
        card = self.deck.cards.first()
        self.deck.deal_card(self.game.player_hand)
        self.assertNotIn(card, self.deck.cards.all())
        self.assertIn(card, self.game.player_hand.all())



class GameLogicTest(TestCase):
    def setUp(self):
        print("\nSetting up the test")
        # Create the Blackjack instance and store it as an instance variable
        self.blackjack = Blackjack()  # This will initialize the Deck and Game
        self.blackjack.start_game()

        # Debug: Print player's hand and dealer's hand
        print("Player's hand:", self.blackjack.player_hand)
        print("Dealer's hand:", self.blackjack.dealer_hand)

    def test_start_game(self):
        pass
        print("\nTesting start_game method")
        # Debug: Print the player's hand
        self.assertEqual(self.blackjack.game.status, 'IN_PROGRESS')
        self.assertEqual(self.blackjack.game.player_hand.count(), 2)
        self.assertEqual(self.blackjack.game.dealer_hand.count(), 2)

        print("\nTesting calculate_score method")
        # Check the player's score
        player_score = self.blackjack.calculate_score(self.blackjack.player_hand)
        print("Player score:", player_score)
        self.assertGreater(player_score, 0)
        
        # Check the dealer's score
        dealer_score = self.blackjack.calculate_score(self.blackjack.dealer_hand)
        print("Dealer score:", dealer_score)
        self.assertGreater(dealer_score, 0)
        
        print("\nTesting get_winner method")
        # Check the winner
        winner = self.blackjack.get_winner()
        print("Winner:", winner)
        self.assertIn(winner, ['Player', 'Dealer', 'Draw'])
        
    def test_hit(self):
        print("\nTesting hit method")
        # Hit the player's hand
        self.blackjack.hit(self.blackjack.game.player_hand)  
        
        # Checking Player Hand now has 3 cards
        self.assertEqual(self.blackjack.game.player_hand.count(), 3)
        
        # Calculating 3 card hand score
        player_score = self.blackjack.calculate_score(self.blackjack.game.player_hand)
        
        # Printing new hand
        print("Player hand after hit:", self.blackjack.game.player_hand.all())  # QuerySet
        #print("Player score after hit:", player_score)
        
        #if player_score == "Bust":
            #self.assertEqual(player_score, "Bust")
        #else:
        #    self.assertGreater(player_score, 0)

        
