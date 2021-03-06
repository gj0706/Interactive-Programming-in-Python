# Basic infrastructure for Bubble Shooter

import simplegui
import random
import math

# Global constants
WIDTH = 800
HEIGHT = 600
FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC = 0.02
BUBBLE_RADIUS = 20
COLOR_LIST = ["Red", "Green", "Blue", "White"]

# global variables
firing_angle = math.pi / 2
firing_angle_vel = 0
bubble_stuck = True


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# class defintion for Bubbles
class Bubble:
    
    def __init__(self, sound = None): # 加声音参数， optional
        # make sure self.pos instance is a list
        # 如果不加list，执行结果是发射器跟小球一起射出
        self.pos = list(FIRING_POSITION) 
        self.vel = [0, 0] # 不是 0 而是一个list
        self.color = random.choice(COLOR_LIST)
        self.sound = sound
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] + BUBBLE_RADIUS >= WIDTH or self.pos[0] <= BUBBLE_RADIUS:
            self.vel[0] = -self.vel[0]
        
    def fire_bubble(self, vel):
        self.vel = vel
        if self.sound:
            self.sound.play()
    def is_stuck(self): 
        pass

    def collide(self, bubble):
        pass
            
    def draw(self, canvas):
        canvas.draw_circle(self.pos, BUBBLE_RADIUS, 2, self.color, self.color)
        

# define keyhandlers to control firing_angle
def keydown(key):
    global a_bubble, firing_angle_vel, bubble_stuck
    if key == simplegui.KEY_MAP["right"]:
        firing_angle_vel -= FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP["left"]:
        firing_angle_vel += FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP["space"]:
        bubble_stuck = False # 小球没有被卡住，也就是开火
        #把发射角度转换成x轴和y轴向量，把小球的速度方向与之匹配
        #使小球射出的方向跟发射的角度一致
        #小球的速度可以是发射器转动的速度，也可以是它的倍数
        bubble_vel = angle_to_vector(firing_angle)
        #小球向上射出，所以y轴速度为负
        a_bubble.fire_bubble([30 * bubble_vel[0], -30 * bubble_vel[1]])
     
        
def keyup(key):
    global firing_angle_vel
    if key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["left"]:
        firing_angle_vel = 0


# define draw handler
def draw(canvas):
    global firing_angle, a_bubble, bubble_stuck

    # update firing angle
    firing_angle += firing_angle_vel
    
    # draw firing line
    upperend_point_vector = [angle_to_vector(firing_angle)[0] * FIRING_LINE_LENGTH, 
                             angle_to_vector(firing_angle)[1] * FIRING_LINE_LENGTH]
    upperend_point_pos = [upperend_point_vector[0] + FIRING_POSITION[0], 
                          FIRING_POSITION[1] - upperend_point_vector[1]]
    canvas.draw_line(FIRING_POSITION, upperend_point_pos, 2, "Yellow")
    # update a_bubble and check for sticking
    a_bubble.update()
    # draw a bubble and stuck bubbles
    a_bubble.draw(canvas)
    
# create frame and register handlers
frame = simplegui.create_frame("Bubble Shooter", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)
# create a sound when firing a bubble
fire_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Collision8-Bit.ogg")
# create initial buble and start frame
a_bubble = Bubble(fire_sound)
frame.start()
