import os
import sys
import cv2
import random
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
try:
    from OpenGL.GL import *
except: pass
pygame.display.init()
pygame.font.init()
sys.path.insert(0, "..")
import sgc
from sgc.locals import *
from sgc.__init__ import __version__ as ver_no
######################################################

#screen size, creating clock
screen = sgc.surface.Screen((1280,720))
clock = pygame.time.Clock()

#elements
# Title
title = sgc.Label(text="Sistema Restaurante ",
                  font=sgc.Font["title"], col=sgc.Font.col)
title.rect.center = (screen.rect.centerx, 40)
title.add()

#buttons
button = sgc.Button(label="Video", pos=(360,100))
button.add(order = 1)

button2 = sgc.Button(label="Cliente", pos=(40,100))
button2.add(order = 1)

button3 = sgc.Button(label="Admin", pos=(200,100))
button3.add(order = 1)

#main
while True:
    time = clock.tick(30)
    for event in pygame.event.get():
        
        sgc.event(event)

        if event.type == GUI:

            if event.widget_type is sgc.Button:
                print "Button event"

            if event.widget is button and event.gui_type == "click":
                

                clip = VideoFileClip('scopRest.avi')
                clip.preview()
                        
        elif event.type == KEYDOWN:
            if event.key == K_f:
                fps.toggle()
        elif event.type == QUIT:
            exit()

    # Cleanup removed windows
   
    if not screen._opengl:
        screen.fill(Color("black"))
    else:
        glClearColor(0,0,1,1)
        glClear(GL_COLOR_BUFFER_BIT)
    # Update the widgets once for each frame
    sgc.update(time)

    pygame.display.flip()
