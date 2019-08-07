# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:34:40 2019

@author: eedo
"""

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT /2
paddle2_pos = HEIGHT / 2
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
player1_score = 0
player2_score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == "RIGHT":
        ball_vel = [random.randrange(120, 240) / 60, - random.randrange(60, 180) / 60]
    elif direction == "LEFT":
        ball_vel = [- random.randrange(120, 240) / 60, - random.randrange(60, 180) / 60]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global player1_score, player2_score  # these are ints
    
    player1_score = 0
    player2_score = 0
    
    x = random.randrange(0, 2)
    if x == 0: 
        spawn_ball("LEFT")
    else:
        spawn_ball("RIGHT")

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel,player1_score, player2_score
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bounce off of top and bottom walls
    if ball_pos[1] <= 0 + BALL_RADIUS: 				
        ball_vel[1] = - ball_vel[1]
        
    if ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), 10, BALL_RADIUS, 'Grey')
    
    # collision with left/right gutters and  determine whether paddle and ball collide 
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel [0] = ball_vel[0] * 1.1
            ball_vel [1] = ball_vel[1] * 1.1
        else:
            spawn_ball("RIGHT")
            player2_score += 1
    elif ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel [0] = ball_vel[0] * 1.1
            ball_vel [1] = ball_vel[1] * 1.1
        else:
            spawn_ball("LEFT")
            player1_score += 1
        
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel[1]
    paddle2_pos += paddle2_vel[1]
    if paddle1_pos <= PAD_HEIGHT / 2:
        paddle1_vel = [0, 0]
        paddle1_pos = PAD_HEIGHT /2
    if paddle1_pos >= HEIGHT - 1 - PAD_HEIGHT / 2:
        paddle1_vel = [0, 0]
        paddle1_pos = HEIGHT - 1 - PAD_HEIGHT /2
        
    if paddle2_pos <= PAD_HEIGHT / 2:
        paddle2_vel = [0, 0]
        paddle2_pos = PAD_HEIGHT /2
    if paddle2_pos >= HEIGHT - 1 - PAD_HEIGHT / 2:
        paddle2_vel = [0, 0]
        paddle2_pos = HEIGHT - 1 - PAD_HEIGHT /2
        
    
    # draw paddles
    canvas.draw_line((PAD_WIDTH / 2, paddle1_pos - PAD_HEIGHT/2),(PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT/2), PAD_WIDTH, "Green")
    canvas.draw_line((WIDTH - PAD_WIDTH/2, paddle2_pos - PAD_HEIGHT/2),(WIDTH - PAD_WIDTH/2, paddle2_pos + PAD_HEIGHT/2), PAD_WIDTH, "RED")
   
        
    # draw scores
    canvas.draw_text(str(player1_score), (150, 100), 80, "White")
    canvas.draw_text(str(player2_score), (450, 100), 80, "White")
                     
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = [0, -6]
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = [0, 6]
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = [0, -6]
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = [0, 6]
    

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = [0, 0]
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = [0, 0]
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = [0, 0]
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = [0, 0]

def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button("Restart", restart)


# start frame
new_game()
frame.start()