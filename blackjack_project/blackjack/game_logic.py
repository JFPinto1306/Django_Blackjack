from .models import Card, Deck, Game

class Blackjack:
    def __init__(self):
        # Ensure a deck exists or create one
        self.deck, _ = Deck.objects.get_or_create()
        if not self.deck.cards.exists():  # Start a new deck if it's empty
            self.deck.start_deck()

        # Ensure a game exists or create one
        self.game, _ = Game.objects.get_or_create()

        # Fetch hands
        self.player_hand = list(self.game.player_hand.all())
        self.dealer_hand = list(self.game.dealer_hand.all())
        
    def calculate_score(self, hand):
        score = 0
        for card in hand:
            card_value = card.get_card_value(score)
            #print(f"Card: {card}, Value: {card_value}")  # Debugging each card
            score += card_value
        #print(f"Final Score: {score}")  # Debugging the total score
        return score if score <= 21 else "Bust"
        
    def start_game(self):
        if not self.deck.cards.exists():
            self.deck.start_deck()
            
        # Reset game state
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()
        self.game.status = "STARTED"
        self.game.save()
        
    def calculate_score(self,hand):
        score = 0
        for card in hand:
            score += int(card.get_card_value(score))
        return score if score <= 21 else "Bust"
        
    def start_game(self):
        self.deck.start_deck()
        #self.deck.shuffle_deck()
        

        # Reset game state
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()
        
        # Starting Game
        self.game.status = "STARTED"
        self.game.save()
        
        # Dealing Player Hand
        self.deck.deal_card(self.game.player_hand)
        self.deck.deal_card(self.game.player_hand)
        
        # Dealing Dealer Hand
        self.deck.deal_card(self.game.dealer_hand)
        self.deck.deal_card(self.game.dealer_hand)
          
        self.game.status = "IN_PROGRESS"
        self.game.save()
        
    def hit(self,hand):
        # Deal one card to the hand
        card = self.deck.deal_card(hand)
        if card:
            hand.append(card)
        return self.calculate_score(hand)
    
    
    def stand(self):
        while self.calculate_score(self.dealer_hand) < 17:  # Dealer hits if score < 17
            self.hit(self.dealer_hand)
        
        return self.get_winner()
    
    
    def get_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        if player_score == "Bust":
            self.game.winner = "Dealer"
        elif dealer_score == "Bust":
            self.game.winner = "Player"
        elif player_score > dealer_score:
            self.game.winner = "Player"
        elif player_score < dealer_score:
            self.game.winner = "Dealer"
        else:
            self.game.winner = "Draw"
        
        self.game.status = "FINISHED"
        self.game.save()
        return self.game.winner