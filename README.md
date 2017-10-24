# Interactive-Programming-in-Python
Exercises and mini projects for this course
# Add an draw method for Tile class

#################################################
# Student adds code where appropriate    

import simplegui

# define globals
TILE_WIDTH = 50
TILE_HEIGHT = 100

# definition of a Tile class
class Tile:
    
    # definition of intializer
    def __init__(self, num, exp, pos):
        self.number = num
        self.exposed = exp
        self.pos = pos
       
    # definition of getter for number
    def get_number(self):
        return self.number
    
    # check whether tile is exposed
    def is_exposed(self):
        return self.exposed
    
    # expose the tile
    def expose_tile(self):
        self.exposed = True
    
    # hide the tile       
    def hide_tile(self):
        self.exposed = False
        
    # string method for tiles    
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    # draw method for tiles
        
    def draw_tile(self, canvas):
        if self.exposed:
            canvas.draw_text(str(self.number), [self.pos[0] + 0.3 * TILE_WIDTH, self.pos[1] - 0.3 * TILE_HEIGHT], 50, "White") 
        else:
            canvas.draw_polygon([self.pos, [self.pos[0] + TILE_WIDTH, self.pos[1]], [self.pos[0] + TILE_WIDTH, 0], [self.pos[0], 0]], 1, "Green", "Green" )
   
    def is_selected(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + TILE_WIDTH:
            return True

def mouseclick(pos):
    if tile1.is_selected(pos):
        tile1.hide_tile()
    if tile2.is_selected(pos):
        tile2.expose_tile()
# draw handler
def draw(canvas):
    tile1.draw_tile(canvas)
    tile2.draw_tile(canvas)
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 2 * TILE_WIDTH, TILE_HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)


# create two tiles.make sure to update initializer  
tile1 = Tile(3, True, [0, TILE_HEIGHT])
tile2 = Tile(5, False, [TILE_WIDTH, TILE_HEIGHT])

# get things rolling
frame.start()
    
    
###################################################
# Resulting frame should display a tile with number 3 (left)
# and a tile with a green back (right)

