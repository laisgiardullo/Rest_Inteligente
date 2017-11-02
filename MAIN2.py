import numpy as np
import cv2
from autocanny import *
from METHODS import *
import Person
import time

cap = cv2.VideoCapture('videos\Fila_Camera1.mp4') #Open video file
#cap = cv2.VideoCapture('videos\Refeitorio_Camera1.mp4') #Open video file
#cap = cv2.VideoCapture('videos\Estavel.mp4') #Open video file
cap.set(3,160) #set width (3) para 160
cap.set(4,90) #set height (4) para 160
persons = []
max_p_age = 5
pid = 1
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=255, detectShadows=True) #Create the background substractor
nframe = 0
old_frame = 0
p0=[]
p1=[]
lista_cx=[]
lista_cy=[]
ret, old_frame = cap.read() #read a frame
a=np.array([]) #todos x na ordem
b=np.array([]) #todos y na ordem
#p0 = [[[468,217]], [[744,211]], [[660,198]], [[692,182]], [[139,121]]]
#p0 = np.ndarray((len(p0), 2), buffer=np.array(p0), dtype=np.float32)
novos_pts = np.dstack((a,b))
novos_pts = novos_pts.astype(np.float32)
while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    tempo_video = cap.get(0)
    #frame2 = Cascade1(frame)
    #frame2 = Countours (frame, fgbg)
    frame2, persons, pid, lista_cx, lista_cy, novos_pts = Countours_Area_Pontual(frame, fgbg, persons, pid, max_p_age,nframe, tempo_video, lista_cx, lista_cy, novos_pts)
    #frame2, persons, pid = Countours_Area(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
    #frame2, persons, pid = Countours_Area_Door(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
    #frame2, persons, pid, old_frame,p0 = Countours_Area_Seguir(frame, fgbg, persons, pid, max_p_age,nframe, tempo_video, old_frame,p0, p1)
    if(novos_pts!=[]):
        novos_pts = novos_pts.reshape(-1,1,2)
    #p0 = np.dstack((lista_cx,lista_cy))
    #p0 = p0.astype(np.float32)
    novos_pts = OptFlow(old_frame, frame, novos_pts) #tem que transformar esses novos pts em p0...
    cv2.imshow('Frame',frame2)
    nframe +=1
    old_frame = frame
    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows