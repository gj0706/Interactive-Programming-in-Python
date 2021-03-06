# Game: RiceRocks(Astroids)
import simplegui
import math
import random

# global constants
WIDTH = 800
HEIGHT = 600
ANGLE_VEL_INC = 0.1
C = 0.1


# global variables
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = sound
            
    def draw(self,canvas): 
        if self.thrust:
            canvas.draw_image(ship_image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        # position update: the ship's motion wraps around the screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # ship's angle update
        self.angle += self.angle_vel
        
        # friction update
        self.vel[0] *= 1 - C
        self.vel[1] *= 1 - C
        
# thrust update: make the ship accelerate forward when thrust

#alternative solution:
#        if self.thrust:
#            acc = angle_to_vector(self.angle)
#            self.vel[0] += acc[0] * .1
#            self.vel[1] += acc[1] * .1

        if self.thrust: 
            fwd_acc = angle_to_vector(self.angle)
            self.vel[0] += fwd_acc[0]
            self.vel[1] += fwd_acc[1]
            
#	alternative solution:    
#    def increment_angle_vel(self):
#        self.angle_vel += .05
#        
#    def decrement_angle_vel(self):
#        self.angle_vel -= .05
        
    def angle_vel_inc(self, inc):
        self.angle_vel += inc
        
    def angle_vel_dec(self, inc):
        self.angle_vel -= inc
        
#    alternative solution:    
#    def set_thrust(self, on):
#        self.thrust = on
#        if on:
#            ship_thrust_sound.rewind()
#            ship_thrust_sound.play()
#        else:
#            ship_thrust_sound.pause()

    def thruster_on(self):
        self.thrust = True
        if self.sound:
            self.sound.play()
    
    def thruster_off(self):
        self.thrust = False
        if self.sound:
            self.sound.rewind()
            
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0],
                      self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 10 * forward[0], 
                       self.vel[1] + 10 * forward[1]]      
        a_missile = Sprite(missile_pos, missile_vel, 0 , 0, 
                           missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
      
        if self.animated == True:
            explosion_index = (self.age % self.lifespan) // 1
            explosion_center = [self.image_center[0] + explosion_index * self.image_size[0],
                                       self.image_center[1]]
            canvas.draw_image(self.image, explosion_center, self.image_size,
                             self.pos, self.image_size, self.angle)
       
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        # angle update
        self.angle += self.angle_vel
        
        # position update: the rock moves and wraps around the screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    def collide(self, other_object):
        other_object_pos = other_object.get_position()
        other_object_radius = other_object.get_radius()
        if dist(self.pos, other_object_pos) <= (self.radius + other_object_radius):
            return True
        else:
            return False
        
def keydown(key): 
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel_inc(ANGLE_VEL_INC) 
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel_dec(ANGLE_VEL_INC) 
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_on()
#alternative solution:     my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
                       
def keyup(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel_dec(ANGLE_VEL_INC)
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel_inc(ANGLE_VEL_INC)    
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_off()
#alternative solution:       my_ship.set_thrust(False)

def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    score = 0
    lives = 3
    timer.start()
    soundtrack.rewind()
    soundtrack.play()
    
def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("lives: " + str(lives), [10, 50], 30, "Yellow" )
    canvas.draw_text("score: " + str(score), [690, 50], 30, "Yellow")
                       
    # draw ship 
    my_ship.draw(canvas)
    
    # update ship 
    my_ship.update()
  
    # update and draw rock and missile group
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # the ship loses one life if hit by a rock
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    # the player gets one score if the missile destroys a rock
    if group_group_collide(rock_group, missile_group):
        score += 1
        
    # if the number of lives reaches 0, game over
    if lives == 0:
        started = False
        rock_group = set([])
        timer.stop()
        soundtrack.pause()
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
     
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    # the max number of rocks on the screen is 12 
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    while dist(rock_pos, my_ship.get_position()) < 150:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * 0.6 - 0.4, random.random() * 0.6 - 0.4]
    rock_angle = 0
    rock_angle_vel = random.random() * 0.3 - 0.1
    a_rock = Sprite(rock_pos, rock_vel, rock_angle, rock_angle_vel, 
                        asteroid_image, asteroid_info)
    # make sure the rock is noe spawned on the ship
    if len(rock_group) < 12:  
        rock_group.add(a_rock)
        
# function that updates missiles and rocks        
def process_sprite_group(group, canvas):
    for sprite in list(group):
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)
    
# check if the ship collides with the rocks
def group_collide(group, other_object):
    for sprite in list(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            explosion = Sprite(sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            return True

# check if missiles and rocks collide         
def group_group_collide(group1, group2):
    for sprite in list(group1):
        if group_collide(group2, sprite):
            group1.discard(sprite)
            return len(group1)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
