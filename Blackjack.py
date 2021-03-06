# Mini-project #6 - Blackjack
# URL: http://www.codeskulptor.org/#user43_gtYsnsTgIc_2.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand_list = []
        
    def __str__(self):
            # return a string representation of a hand
        hand = ""
        for i in range(len(self.hand_list)):
            hand += str(self.hand_list[i]) + " "
        return "Hand contains " + hand 
    
    def add_card(self, card):
        return self.hand_list.append(card) 	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        has_ace = False
        for card in self.hand_list:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == "A": 
                has_ace = True
        if hand_value + 10 <= 21 and has_ace == True:
            hand_value += 10
  
        return hand_value
                                       
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand_list:
            card.draw(canvas, pos)
            pos[0] += 90
        
# define deck class 
class Deck:
    def __init__(self):
            # create a Deck object
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck_list.append(card)              

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        return random.shuffle(self.deck_list)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck_list.pop()
    
    def __str__(self):
        # return a string representing the deck
        deck = ""
        for i in range(len(self.deck_list)):
            deck += str(self.deck_list[i]) + " "
        return "Deck contains "  + deck  


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    if in_play == True:
        score -= 1
        in_play = False
        outcome = "You give up. New deal?"
    else:
        deck = Deck()
        player = Hand()
        dealer = Hand()
        deck.shuffle()
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        outcome = "Hit or stand?"
        in_play = True
        
def hit():
    global in_play, deck, player, dealer, score, outcome
    # if the hand is in play, hit the player
    if in_play == True:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and
            if player.get_value() > 21: 
                outcome = "You have busted. Try again? "
                in_play = False
                score -= 1
       
def stand():
    global in_play, deck, player, dealer, outcome, score, outcome
    
    while in_play == True:
    
        if dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        elif dealer.get_value() > 21:
            outcome = "Dealer has busted, you win!"
            score += 1
            in_play = False
        elif dealer.get_value() >= player.get_value():
            outcome = "You lose! One more time?"
            score -= 1
            in_play = False
        elif dealer.get_value() < player.get_value(): 
            outcome = "Bravo! You win! Play again?"
            score += 1
            in_play = False
        else:
            outcome = "You lose! One more time?"
            score -=1
            in_play = False
        if player.get_value() > 21:
            outcome = "You have busted. Try again?"
            score -=1
            in_play = False
                 
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play
    canvas.draw_text(outcome, [300, 300], 20, "White")
    canvas.draw_text("Blackjack", [250, 50], 30, "Black")
    canvas.draw_text("Score = " + str(score), [300, 140], 20, "White")
    canvas.draw_text("Dearler", [40, 140], 20, "Yellow")
    canvas.draw_text("Player", [40, 300], 20, "Yellow")
    dealer.draw(canvas, [40, 170])
    player.draw(canvas, [40, 330])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [(CARD_BACK_CENTER[0] + 130), (CARD_BACK_CENTER[1] + 170)], CARD_BACK_SIZE )
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
