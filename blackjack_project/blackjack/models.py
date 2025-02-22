from django.db import models
import random

# Create your models here.

class Card(models.Model):
    SUIT_CHOICES = [
        ('Hearts', 'Hearts'),
        ('Diamonds', 'Diamonds'),
        ('Clubs', 'Clubs'),
        ('Spades', 'Spades'),
    ]
    VALUE_CHOICES = [
        ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('J', 'Jack'),
        ('Q', 'Queen'), ('K', 'King'), ('A', 'Ace'),
    ]
    
    value = models.CharField(max_length=5, choices=VALUE_CHOICES)
    suit = models.CharField(max_length=10, choices=SUIT_CHOICES)
    
    is_dealt = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def get_card_value(self, current_score=0):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            # Ace value is 11 unless it causes a bust (score > 21), in which case it is 1
            if current_score + 11 > 21:
                return 1
            else:
                return 11
        else:
            return int(self.value)


class Game(models.Model):
    
    STATUS_CHOICES = [
        ('STARTED', 'Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]    
    # Game Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='STARTED')
    
    player_hand = models.ManyToManyField(Card, related_name='player_cards')
    dealer_hand = models.ManyToManyField(Card, related_name='dealer_cards')
    
    player_score = models.IntegerField(default=0)
    dealer_score = models.IntegerField(default=0)
    winner = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Game {self.id} - Status: {self.status}"    


class Deck(models.Model):
    cards = models.ManyToManyField(Card)

    def shuffle_deck(self):
        # Shuffle the cards in the deck by fetching the cards into a list
        cards = list(self.cards.all())  # Convert ManyToMany to a list
        random.shuffle(cards)  # Shuffle the list of cards
        self.cards.set(cards)  # Update the deck with shuffled cards

    def start_deck(self):
        # Create a full deck of 52 cards at the start of the game
        new_cards = []
        for suit_choice in Card.SUIT_CHOICES:  # Using Card's SUIT_CHOICES
            for value_choice in Card.VALUE_CHOICES:  # Using Card's VALUE_CHOICES
                # Create each card instance based on the choices
                card = Card.objects.create(suit=suit_choice[0], value=value_choice[0])
                new_cards.append(card)

        # Add cards to the deck
        self.cards.set(new_cards)  # This sets all the created cards to the deck
        self.shuffle_deck()  # Shuffle the cards once they are added
        self.save()

    def deal_card(self,hand):
        # Deal a card from the deck
        card = self.cards.first()
        card.is_dealt = True
        
        # Remove the dealt card from the deck
        self.cards.remove(card)
        self.save()
        
        hand.add(card)
        return card
    
    def reset_deck(self):
        # This could be used to reset the deck in case you want to reinitialize it after a round
        self.cards.clear()  # Remove all cards from the deck
        self.start_deck()  # Recreate and shuffle the deck
        self.save()

    def remaining_cards(self):
        return self.cards.count()  # Return how many cards are left in the deck
