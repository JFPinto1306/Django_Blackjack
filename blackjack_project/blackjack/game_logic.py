from .models import Card, Deck, Game

class Blackjack:
    def __init__(self,game_id=None):
        if game_id:
            # Load an existing game
            self.game = Game.objects.get(id=game_id)
            self.deck = self.game.deck
            self.player_hand = self.game.player_hand
            self.dealer_hand = self.game.dealer_hand
            
        else:
            # Ensure a game exists or create one
            self.game = Game.objects.create()

            # Ensure a deck exists or create one
            self.deck = Deck.objects.create(game=self.game)

            # Fetch hands directly using ManyToManyManager (no need for list conversion)
            self.player_hand = self.game.player_hand
            self.dealer_hand = self.game.dealer_hand

    def calculate_score(self, hand):
        score = 0
        for card in hand.all():
            score += card.get_card_value(score)
        return score 

    def start_game(self):
        self.deck.start_deck()

        # Reset game state
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()

        # Starting Game
        self.game.status = "STARTED"
        self.game.save()

        # Dealing Player Hand
        self.deck.deal_card(self.player_hand)
        self.deck.deal_card(self.player_hand)

        # Dealing Dealer Hand
        self.deck.deal_card(self.dealer_hand)
        self.deck.deal_card(self.dealer_hand)
        
        # Calculate scores
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        # Update game with scores
        self.game.player_score = player_score
        self.game.dealer_score = dealer_score
        
        #print(f"\n\nDebugging Start Game. \n Scores:\n - Player: {player_score}, \n - Dealer: {dealer_score}")  # Debugging line for scores

        self.game.status = "IN_PROGRESS"
        self.game.save()

        #print(f"Game saved: {self.game.id}, Player Score: {self.game.player_score}, Dealer Score: {self.game.dealer_score}\n\n")  # Debugging line to check if changes persist

    def hit(self, hand):
        if self.game.status == "IN_PROGRESS":
            # Deal one card to the hand
            card = self.deck.deal_card(hand)  # This will deal a card from the deck and add it to the hand
        else:
            pass

        return self.calculate_score(hand)

    def stand(self):
        # If player stands, go to get_winner
        return self.get_winner()

    def get_winner(self):

        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        
        if player_score > 21:
            self.game.winner = "Dealer"        
            #self.game.status = "FINISHED"
            #self.game.save()
            #    
            #return self.game.winner
            
        else:
            # Dealer hits until he reaches 17
            while dealer_score <= 21:
                while int(dealer_score) < 17:
                    self.hit(self.dealer_hand)
                    print("Dealer hand after hit (Dealer hits until reaches 17):", self.dealer_hand.all())
                    dealer_score = self.calculate_score(self.dealer_hand)
                    print("Dealer score after hit:", dealer_score)
                    if dealer_score > 21:
                        self.game_winner = "Player"
                        break
                break
                
            if dealer_score > 21:
                self.game.winner = "Player"
            elif player_score > dealer_score:
                self.game.winner = "Player"
            elif player_score < dealer_score:
                self.game.winner = "Dealer"
            else:
                self.game.winner = "Draw"


        # Update game with scores
        self.game.player_score = player_score
        self.game.dealer_score = dealer_score        
        self.game.status = "FINISHED"
        self.game.save()
            
        return self.game.winner
