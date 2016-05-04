# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite -949*392 -source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")


# initialize some useful global variables
in_play = False
score = 0
outcome = "Hit or Stand?"
sMessage = ""

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
        canvas.draw_image(card_image, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], 
                           pos[1] + CARD_CENTER[1]], 
                          CARD_SIZE)
        
    def drawBack(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, 
                          [pos[0] + CARD_BACK_CENTER[0] + 1, 
                           pos[1] + CARD_BACK_CENTER[1] + 1], 
                          CARD_BACK_SIZE)
        
class Hand:
    def __init__(self):
        self.cards = []
    
    def __str__(self):
        sCards = ""
        for card in self.cards:
            sCards = sCards + str(card) + " "
        return "Hand contains " + sCards.strip()
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_value(self):
        sum = 0
        for card in self.cards:
            sum += VALUES[card.get_rank()]
        for card in self.cards:
            if card.get_rank() == RANKS[0]:
                if sum + 10 <= 21:
                    sum += 10
        return sum
    
    def busted(self):

        if self.get_value() > 21:
            return True
        else:
            return False
            
    
    def draw(self, canvas, p):
        for card in self.cards:
            p[0] = p[0] + CARD_SIZE[0] + 20
            card.draw(canvas, p)
    
    
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()
        
    
def deal():
    global outcome, inplay, deck, player, dealer, in_play
    
    
    deck = Deck()
    player = Hand()
    dealer = Hand()
    
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    

    
    in_play = True
    
def hit():
    global in_play, player, outcome, sMessage, score
    
    if in_play:
        player.add_card(deck.deal_card())
    
        if player.busted():
            sMessage = "You went bust and lose."
            outcome = "New deal?"
            score -= 1
            in_play = False

def stand():
    global dealer, in_play, sMessage, score
    
    if in_play:
        in_play = False

        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

        if dealer.get_value() > 21:
            sMessage = "You win."
            score += 1
        elif dealer.get_value() > player.get_value():
            sMessage =  "You lose."
            score -= 1
        elif dealer.get_value() < player.get_value():
            sMessage = "You win."
            score += 1
        else:
            sMessage =  "You lose."
            score -= 1
            
        outcome = "New deal?"

def draw(canvas):
    global hand, in_play
    
    canvas.draw_text("Blackjack", (60, 100), 40, "Aqua")
    canvas.draw_text("Dealer", (60, 185), 33, "Black")
    canvas.draw_text("Player", (60, 385), 33, "Black")
    canvas.draw_text(outcome, (250, 385), 33, "Black")
    canvas.draw_text(sMessage, (250, 185), 25, "Black")
    canvas.draw_text("Score: " + str(score), (450, 100), 33, "Black")
    
    player.draw(canvas, [-65, 400])
    dealer.draw(canvas, [-65, 200])
    
    if in_play:
        dealer.cards[0].drawBack(canvas, [28,200])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
deal()
    

    
    