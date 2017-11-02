#fonte: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
import numpy as np
import cv2
from autocanny import *
import Person
import time
from FUNCTIONS import *
#inicializacao de variaveis
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)
areaTH = 100 # areaTH=area minima para considerar uma pessoa
#Inicializacao de contadores
num_pessoas = 0
i=0
n_cont=0
n_frame = 0
vetores_x=[]
vetores_y=[]
cap = cv2.VideoCapture('videos\Fila_Camera1.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=255, detectShadows=True) #Create the background substractor

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
 
# Create some random colors
#se der mts pontos, mudar o primeiro elemento do ultimo parametro (num_cores,x)
color = np.random.randint(0,255,(400,3))

while(n_frame<=22):
    ret, old_frame = cap.read()
    if(n_frame==22):
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        #Aplicacao do substractor
        fgmask = fgbg.apply(old_frame) #Use the substractor: aqui, o fundo, que nao esta mexendo, fica preto e o que esta se movimentando branco
        try:
            mask = Aplicacao_Mascara(fgmask)
        except:
            #se nao tem mais imagens para mostrar...
            print('EOF')
        __, contours1, hierarchy1 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        #print("p1: "+str(p1))
        for cnt in contours1:
            #cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
            area = cv2.contourArea(cnt)
            
            #########   LINK   ###########
            #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
            x,y,w,h = cv2.boundingRect(cnt) # x e y: top left
            if(area>areaTH):
                guard_x=x
                inter_x = w/4
                inter_y = h/4
                print("estouaqui")
                
                while(guard_x<x+w):
                    print("entrei")
                    guard_y=y
                    while(guard_y<y+h):
                        #print ("y:"+str(y))
                        #print ("guard_y:"+str(y))
                        #print("inter_y:"+str(inter_y))
                        esta_dentro= cv2.pointPolygonTest(cnt, (guard_x,guard_y) , False) #testar se ponto esta mesmo dentro do contorno
                        if(esta_dentro):
                            vetores_x.append([guard_x])
                            vetores_y.append([guard_y])
                        guard_y=guard_y+inter_y
                    guard_x+=inter_x
                

        #p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        #a=np.array([[468.],[744.], [660.], [692.], [139.]]) #todos x na ordem
        #b=np.array([[217.],[211.], [198.], [182.], [121.]]) #todos y na ordem
        #p0 = [[[468,217]], [[744,211]], [[660,198]], [[692,182]], [[139,121]]]
        #p0 = np.ndarray((len(p0), 2), buffer=np.array(p0), dtype=np.float32)
        p0 = np.dstack((vetores_x,vetores_y))
        #print(p0)
        p0 = p0.astype(np.float32)
        #print(p0)
        #print(p0.dtype)
        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame)
        #a=[]
        #b=[]
        #n_frame+=1
    n_frame+=1

while(cap.isOpened()):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    print(p1)  
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        #mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        #frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        mask = cv2.line(mask, (a,b),(c,d), (0,255,0), 2)
        frame = cv2.circle(frame,(a,b),5,(0,255,0),-1)
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
