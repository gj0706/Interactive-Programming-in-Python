# implementation of card game - Memory

import simplegui
import random

#define global variables
num_list = list(range(0, 8))
list1 = list(range(0, 8))
num_list.extend(list1)
exposed = list(range(16))

CARD_WIDTH = 50
CARD_HEIGHT = 100

# helper function to initialize globals
def new_game():
    global exposed, state, turns
    for i in range(16):
        exposed[i] = False
    state = 0
    turns = 0
    random.shuffle(num_list)
    
# define event handlers
def mouseclick(pos):
    global exposed, state, first_click, second_click, turns
    i = pos[0] // CARD_WIDTH
    if not exposed[i]:
        if state == 0:
            exposed[i] = True
            first_click = i
            state = 1
            turns += 1
        elif state == 1:
            exposed[i] = True
            second_click = i
            state = 2
        else:
            if num_list[first_click] != num_list[second_click]:
                exposed[first_click] = False
                exposed[second_click] = False
            first_click = i
            exposed[i] = True
            state = 1
            turns += 1       
              
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = " + str(turns))
    global exposed
    for i in range(len(num_list)):
        if exposed[i] == True:
            canvas.draw_text(str(num_list[i]), [i * CARD_WIDTH, CARD_HEIGHT- 15], CARD_HEIGHT, "White")        
        else:
            canvas.draw_polygon([[i * CARD_WIDTH, 0], [(i + 1) * CARD_WIDTH, 0], [(i + 1) * CARD_WIDTH, CARD_HEIGHT], [i * CARD_WIDTH, CARD_HEIGHT]], 1, "Black", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
