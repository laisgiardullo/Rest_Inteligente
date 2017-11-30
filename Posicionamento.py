import numpy as np
import cv2
#from autocanny import *
from METHODS import *
import Person
import time
import sqlite3 as lite
import sys

from variaveis_globais import * #w_frame etc aqui
from MatrizPixels import *
from Deteccao import *
from ApoioDeteccao import *
from CaracteristicasCalculadas import *

def OptFlow(old_frame, frame, p0, mask):
            #fonte: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
     
    # Create some random colors
    #color = np.random.randint(0,255,(100,3))
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    print("p1: "+str(p1))

     # Select good points
    #good_new = p1[st==1] #status==1: flow foi encontrado
    #good_old = p0[st==1]
    #print("good_new:"+str(good_new))
    #print("good_old:"+str(good_new))
    # # draw the tracks

    # #ZIP x = [1, 2, 3], y = [4, 5, 6], zip(x, y) =[(1, 4), (2, 5), (3, 6)]
    # #ENUMERATE seasons = ['Spring', 'Summer', 'Fall', 'Winter'], list(enumerate(seasons)) = [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
    # # i = numero do enumerate, new = elemento do good_new, old = elemento do good_old
    # for i,(new,old) in enumerate(zip(good_new,good_old)):
    for i,(new,old) in enumerate(zip(p1,p0)):
        a,b = new.ravel() #ravel: A 1-D array, containing the elements of the input, is returned
        c,d = old.ravel()
        #if((a,b)!=(c,d)):
        mask = cv2.line(mask, (a,b),(c,d), (0,255,0), 2)
        frame = cv2.circle(frame,(a,b),5,(0,255,0),-1)

    img = cv2.add(frame,mask)

    cv2.imshow('frame_22',img)

    # # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    # #p0 = good_new.reshape(-1,1,2)
    #if(len(good_new)==len(p1)):
    #    try:
    #        print("gnr:"+str(good_new.reshape(-1,1,2)))
    #        good_new = good_new.reshape(-1,1,2) #voltar ao formato original de p0
    #        novos_pts = good_new
    #    except:
    #        pass
    novos_pts = p1
    return (novos_pts, mask)
def OptFlowDense(old_frame, frame):
	mask = np.zeros_like(frame)
	next = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	prvs = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
	flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
	return(flow)