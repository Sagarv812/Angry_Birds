import pygame, sys, time

pygame.init()

g = 9.81 #acceleration due to gravity
scale = 50 #scale: 50 pixels is 1 meter

#template(old pixel count, time b/w two frames in milliseconds, speed in pixels/s)
def newPosition(time,speed):
    global g

    speed[1] += g*time
    move = [speed[0]*time*scale,(speed[1]*time + 0.5*g*(time**2))*scale]
    return move


    

