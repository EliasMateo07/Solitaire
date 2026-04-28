import pygame
import sys
import random
"""
Found Errors
moving a column from an empty stack to another empty stack: 
King hides under stack for some reason

When extra stack is empty it throws an error

Moving cards out of pile
"""
# Initialize Pygame
pygame.init()
GREEN = (0,128,128)
BLACK = (0,0,0)

def bring_to_front(sprite_group, sprite):
    ###Bring the specified sprite to the front of the sprite group.###
    sprite_group.remove(sprite)
    sprite_group.add(sprite)

def is_not_colliding(rect_to_check, other_rects):
    for rect in other_rects:
        if rect_to_check.rect.colliderect(rect.rect):
            if rect_to_check == rect:
                break
            return False
    return True
    
def cards_collision(all_sprites):
    list = []
    for card in all_sprites:
        if card.rect.collidepoint(event.pos):
            if card.flipped:
                list.append(card)
    list = sorted(list, key=lambda card: int(card.value))
    return list

def valid_move(card, top_card):
    if int(card.value) == int(top_card.value) - 1:
        if (card.suit in ['Hearts', 'Diamonds'] and top_card.suit in ['Clubs', 'Spades']) or \
           (card.suit in ['Clubs', 'Spades'] and top_card.suit in ['Hearts', 'Diamonds']):
            print("valid_move")
            return True
        elif top_card.suit is None:
            return True
    return False

def pile_valid_move(card, pile):
    if int(card.value) == int(pile.value) and card.suit == pile.suit:
        return True
    else:
        return False
    
def all_piles_filled(Piles):
    for pile in Piles:
        if pile.value != 13:  # Assuming max_pile_value is the maximum value a pile can have
            return False
    return True
def all_cards_flipped(all_sprites):
    for sprite in all_sprites:
        if not sprite.flipped:  # Assuming max_pile_value is the maximum value a pile can have
            return False
    return True

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 910, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solitaire")

# Load card back image
CardBack = pygame.image.load("BackCard.png")
card_width, card_height = CardBack.get_width(), CardBack.get_height()
EmptyPile = pygame.image.load("CardPiles/EmptyPile.png")

# Define the rectangle for the current frame
frame_rect = pygame.Rect(0, 0, card_width, card_height)

# Card class
class Card(pygame.sprite.Sprite):
    def __init__(self, image_back, image_front, suit, value, x, y):
        super().__init__()
        self.suit = suit
        self.value = value
        self.image_back = image_back
        self.image_front = image_front
        self.image = image_back  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.flipped = False  
        
    def flip(self):
        if not self.flipped:
            self.image = self.image_front 
            self.flipped = True
        else:
            self.image = self.image_back
            self.flipped = False
        
# Create card instances for each card
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
x = 10
y = 20


deck = []
# Create card instances for each card
for suit in suits:
    for value in values:
        # Load card images
        card_front = pygame.image.load(f"extracted_cards/{suit}/card_{value}.png")
        card_back = CardBack
        card = Card(card_back, card_front, suit, value, x, y)
        deck.append(card)
        
random.shuffle(deck)        
Empty = Card(EmptyPile, EmptyPile, None, 0, x, y)
all_sprites = pygame.sprite.Group(deck)
deck.insert(0, Empty)
Empty.flip()

# Group for card sprites
extra_cards = []

column1 = []
column2 = []
column3 = []
column4 = []
column5 = []
column6 = []
column7 = []
all_columns = [column1, column2, column3, column4, column5, column6, column7]

column1.append(deck.pop())
for i in range(2):
    column2.append(deck.pop())
for i in range(3):
    column3.append(deck.pop())
for i in range(4):
    column4.append(deck.pop())
for i in range(5):
    column5.append(deck.pop())
for i in range(6):
    column6.append(deck.pop())
for i in range(7):
    column7.append(deck.pop())

Empty_Piles = []
i = 0
for column in all_columns:
    i += 1
    j = 0
    Empty = Card(EmptyPile, EmptyPile, None, 14, (10 + (100 * i)), y)
    Empty_Piles.append(Empty)
    Empty.image.fill(GREEN)
    all_sprites.add(Empty)
    Empty.flip()
    for card in column:
        j += 1
        card.rect.x = 10 + (100 * i)
        card.rect.y = 20 * j
        bring_to_front(all_sprites, card)
        
        if j == 7: 
            j = 0
    column.insert(0, Empty)

top_card_list = []
for column in all_columns:
    top_card_list.append(column[-1])
for card in top_card_list:
        card.flip()

x_decks = 810
y = 460
Piles=[]

Heartpile = pygame.image.load("CardPiles\HeartPile.png")
Hearts = Card(Heartpile, None, 'Hearts', 1, x_decks, y)
Piles.append(Hearts)
heart_pile = [Hearts]

Spadepile = pygame.image.load("CardPiles\Spadepile.png")
Spades = Card(Spadepile, None, 'Spades', 1, x_decks, 15)
Piles.append(Spades)
spade_pile = [Spades]

Clubpile = pygame.image.load("CardPiles\ClubPile.png")
Clubs = Card(Clubpile, None, 'Clubs', 1, x_decks, y-150)
Piles.append(Clubs)
club_pile = [Clubs]

Diamondpile = pygame.image.load("CardPiles\Diamondpile.png")
Diamonds = Card(Diamondpile, None, 'Diamonds', 1, x_decks, y-300)
Piles.append(Diamonds)
diamond_pile = [Diamonds]
piles_list = [heart_pile, spade_pile, club_pile, diamond_pile]
all_columns.extend(piles_list)


dragging = False
dragging_multiple = False
deck_used = False
running = True
valid_move_used = False
pile_move_used = False
grabbed_card = None
cards_over = []
i = 0

#Track Pile Values
for pile in Piles:
    all_sprites.add(pile)
    
# Main game loop
while running:
    screen.fill(GREEN)
    for column in all_columns:
        try:
            top_card = column[-1]
        
            if top_card not in top_card_list:
                top_card_list.append(top_card)
        except:
            continue
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ### GRABBING CARDS FROM COLUMNS
                if not dragging: 
                    for column in all_columns:
                        for card in column:
                            if card.rect.collidepoint(event.pos):
                                if card.flipped and card not in Empty_Piles:
                                    if column[-1] == card:
                                        origin_column = column
                                        bring_to_front(all_sprites, card)
                                        
                                        dragging = True
                                        grabbed_card = card
                                        origin_x = card.rect.x
                                        origin_y = card.rect.y
                                        drag_offset_x = card.rect.x - event.pos[0]
                                        drag_offset_y = card.rect.y - event.pos[1]
                                    else:
                                        dragging_multiple = True
                                        list = cards_collision(all_sprites)
                                        if list[0] != card:
                                            card = list[0]
                                        grabbed_card = card
                                        origin_column = column
                                        origin_x = card.rect.x
                                        origin_y = card.rect.y
                                        index_card = column.index(card)
                                        bring_to_front(all_sprites, card)
                                        drag_offset_x = card.rect.x - event.pos[0]
                                        drag_offset_y = card.rect.y - event.pos[1]

                                        for element in column[index_card + 1:]:
                                            cards_over.append(element) 
                                        
                                        for card in cards_over:
                                            bring_to_front(all_sprites, card)
                                            card.origin_x = card.rect.x
                                            card.origin_y = card.rect.y
                                            card.drag_offset_x = card.rect.x - event.pos[0]
                                            card.drag_offset_y = card.rect.y - event.pos[1]
                                               

                    ### DECK CARD USAGE
                    if extra_cards:
                        if extra_cards[-1].rect.collidepoint(event.pos):
                            bring_to_front(all_sprites, extra_cards[-1])
                            origin_column = extra_cards
                            dragging = True
                            grabbed_card = extra_cards[-1]
                            origin_x = extra_cards[-1].rect.x
                            origin_y = extra_cards[-1].rect.y
                            drag_offset_x = extra_cards[-1].rect.x - event.pos[0]
                            drag_offset_y = extra_cards[-1].rect.y - event.pos[1]

               ### CLICKING ON DECK ###
            
                if deck[-1].rect.collidepoint(event.pos):
                    if deck_used:
                        for card in extra_cards:
                            card.rect.y = -500

                    if deck[-1].value == 0: 
                        print("empty func")
                        print(len(deck), len(extra_cards))
                        extra_cards.reverse()
                        while extra_cards:
                            for card in extra_cards:
                                card.flip()
                                card.rect.y = 20
                                bring_to_front(all_sprites, card)
                                extra_cards.remove(card)
                                deck.append(card)
                        print(len(deck), len(extra_cards))
                        
                    else:    
                        for k in range(3):
                            if deck[-1].value != 0: 
                                deck[-1].flip()
                                deck[-1].rect.y += (130 + (k*25))
                                bring_to_front(all_sprites, deck[-1])
                                extra_cards.append(deck[-1])
                                deck.pop()
                                deck_used = True
                        print(len(deck), len(extra_cards))
                        

        ### VALID MOVES ####                                        
        elif event.type == pygame.MOUSEBUTTONUP:    
            if event.button == 1:
                ### SINGLE CARD ###
                if dragging:
                    for sprite in all_sprites:
                        if grabbed_card == sprite:
                            continue
                        elif grabbed_card.rect.colliderect(sprite) or sprite.rect.collidepoint(event.pos):
                            if sprite.flipped or sprite in Piles or sprite == Empty:
                                if valid_move(grabbed_card, sprite):
                                    for column in all_columns:
                                        if sprite in column and sprite in top_card_list: 
                                            grabbed_card.rect.x = sprite.rect.x
                                            if sprite.value == 14:
                                                grabbed_card.rect.y = sprite.rect.y
                                            else:
                                                grabbed_card.rect.y = sprite.rect.y + 25
                                            top_card_list.remove(sprite)
                                            origin_column.remove(grabbed_card)
                                            try:
                                                if not origin_column[-1].flipped:
                                                    origin_column[-1].flip()
                                                column.append(grabbed_card)
                                            except IndexError as e:
                                                print(e)
                                                
                                            valid_move_used = True
                                    break

                                elif pile_valid_move(grabbed_card, sprite):
                                    for pile in piles_list:
                                        if sprite in pile:
                                            pile.append(grabbed_card)
                                    grabbed_card.rect.x = sprite.rect.x
                                    grabbed_card.rect.y = sprite.rect.y
                                    sprite.value += 1
                                    origin_column.remove(grabbed_card)
                                    pile_move_used = True
                                    try:
                                        if not origin_column[-1].flipped:
                                            origin_column[-1].flip()
                                        break
                                    except:
                                        break
                ### MULTIPLE CARDS ### 
                elif dragging_multiple:
                    for sprite in all_sprites:
                        if grabbed_card.rect.colliderect(sprite) and sprite.rect.collidepoint(event.pos):
                            if sprite.flipped or sprite in Piles:
                                if grabbed_card == sprite:
                                    continue
                                elif sprite in cards_over:
                                    continue
                                elif valid_move(grabbed_card, sprite):
                                    for column in all_columns:
                                        if sprite in column and sprite in top_card_list:
                                            grabbed_card.rect.x = sprite.rect.x
                                            if sprite.value == 14:
                                                grabbed_card.rect.y = sprite.rect.y
                                            else:
                                                grabbed_card.rect.y = sprite.rect.y + 25
                                                
                                            top_card_list.remove(sprite)
                                            origin_column.remove(grabbed_card)
                                            valid_move_used = True
                                            column.append(grabbed_card)

                                            for i, card in enumerate(cards_over, start=1):
                                                origin_column.remove(card)
                                                column.append(card)
                                                card.rect.x = sprite.rect.x
                                                card.rect.y = grabbed_card.rect.y + (25 * i)
                                            if not origin_column[-1].flipped:
                                                origin_column[-1].flip()
                                    break
                ### INVALID MOVES ###
                if not valid_move_used and not pile_move_used:
                    try:
                        if dragging:
                            grabbed_card.rect.x = origin_x
                            grabbed_card.rect.y = origin_y  
                        elif dragging_multiple:
                            grabbed_card.rect.x = origin_x
                            grabbed_card.rect.y = origin_y      
                            for card in cards_over:
                                card.rect.x = card.origin_x
                                card.rect.y = card.origin_y   
                    except:
                        continue

                dragging_multiple = False
                dragging = False
                valid_move_used = False
                pile_move_used = False
                grabbed_card = None 
                cards_over.clear()

        ### MOTION ###
        elif event.type == pygame.MOUSEMOTION:
            if dragging: # SINGLE
                if grabbed_card is not None:
                    grabbed_card.rect.x = event.pos[0] + drag_offset_x
                    grabbed_card.rect.y = event.pos[1] + drag_offset_y
            elif dragging_multiple: # MULTIPLE
                if grabbed_card is not None:       
                    for card in cards_over:
                        card.rect.x = event.pos[0] + card.drag_offset_x
                        card.rect.y = event.pos[1] + card.drag_offset_y
                    grabbed_card.rect.x = event.pos[0] + drag_offset_x
                    grabbed_card.rect.y = event.pos[1] + drag_offset_y

    if all_piles_filled(Piles):
        print("YOU WIN")
    if all_cards_flipped(all_sprites):
        print("WIN!, TRY AND COMPLETE THE SUITS!")
    # Draw all sprites
    all_sprites.draw(screen)    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()