import numpy as np
import cv2
from autocanny import *
import Person
import time
persons = []
pid = 0
p = Person.MyPerson(pid,20,20, 4, "in")
persons.append(p)
pid += 1

for i in persons:
    #print (i.getX())
    #print("NOVOX"+str(new_x)+"WIDTH"+str(new_width))
    #if abs(cx-i.getX()) <= new_width and abs(cy-i.getY()) <= h:
    #if abs(new_x-i.getX()) <= new_width and abs(y-i.getY()) <= h:
    # se antigo centro estiver dentro do mesmo retangulo novo.. Ainda e o mesmo 
    i.updateCoords(20,30)   #actualiza coordenadas en el objeto and resets ag
    i.updateCoords (40,20)

for i in persons:
    print (" ")
    print ("Pessoas:")
    print ("id:"+str(i.i))
    print(i.x)
    print(i.y)
    print (i.tracks)
    print (i.status)