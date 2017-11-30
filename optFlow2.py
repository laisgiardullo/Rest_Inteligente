import cv2
import numpy as np
from variaveis_globais import *
cap = cv2.VideoCapture('videos\Eletrica_Ent.mov')
#cap = cv2.VideoCapture('videos\Rest_Israel.mp4') #Open video file

ret, frame1 = cap.read()
frame1 = cv2.resize(frame1, (w_frame, h_frame))
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
x_ant = 409
y_ant = 95

x_ant2 = 409
y_ant2 = 100

x_ant3 = 415
y_ant3 = 80

x_ant4 = 250
y_ant4 = 195

x_ant5 = 350
y_ant5 = 195


num_frame = 0
flow = [0]
while(1):
    ret, frame2 = cap.read()
    frame2 = cv2.resize(frame2, (w_frame, h_frame))
    mask = np.zeros_like(frame2)
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    num_frame+=1
    if (num_frame%10==0):
        if (len(flow)==1):
            flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        else:
            flow = cv2.calcOpticalFlowFarneback(prvs,next, flow, 0.5, 3, 15, 3, 5, 1.2, 0)
        print(flow)
        print(len(flow))
        print("--")
        testex = flow[int(y_ant)][int(x_ant)][0]
        testey = flow[int(y_ant)][int(x_ant)][1]
        print(str(testex)+","+str(testey))
        x = testex + x_ant
        y = testey + y_ant
        mask = cv2.line(mask, (int(x_ant),int(y_ant)),(int(x),int(y)), (0,255,0), 2)
        mask = cv2.putText(mask, "AQUI", (int(x),int(y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
        mask = cv2.circle(mask,(int(x),int(y)),5,(0,255,0),-1)
        x_ant = x
        y_ant = y

        x2 = int(flow[y_ant2][x_ant2][0] + x_ant2)
        y2 = int(flow[y_ant2][x_ant2][1] + y_ant2)
        mask = cv2.line(mask, (x_ant2,y_ant2),(x2,y2), (0,255,0), 2)
        mask = cv2.putText(mask, "AQUI", (x2, y2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
        x_ant2 = x2
        y_ant2 = y2

        x3 = int(flow[y_ant3][x_ant3][0] + x_ant3)
        y3 = int(flow[y_ant3][x_ant3][1] + y_ant3)
        mask = cv2.line(mask, (x_ant3,y_ant3),(x3,y3), (0,255,0), 2)
        mask = cv2.putText(mask, "AQUI", (x3, y3), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
        x_ant3 = x3
        y_ant3 = y3

        x4 = int(flow[y_ant4][x_ant4][0] + x_ant4)
        y4 = int(flow[y_ant4][x_ant4][1] + y_ant4)
        mask = cv2.line(mask, (x_ant4,y_ant4),(x4,y4), (0,255,0), 2)
        mask = cv2.putText(mask, "AQUI", (x4, y4), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
        x_ant4 = x4
        y_ant4 = y4

        x5 = int(flow[y_ant5][x_ant5][0] + x_ant5)
        y5 = int(flow[y_ant5][x_ant5][1] + y_ant5)
        mask = cv2.line(mask, (x_ant5,y_ant5),(x5,y5), (0,255,0), 2)
        mask = cv2.putText(mask, "AQUI", (x5, y5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
        x_ant5 = x5
        y_ant5 = y5

        frame2 = cv2.add(frame2,mask)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        prvs = next

        cv2.imshow('frame2',rgb)
        cv2.imshow('frame_optflow',frame2)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.imshow('frame2',rgb)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png',frame2)
            cv2.imwrite('opticalhsv.png',rgb)
    #prvs = next

cap.release()
cv2.destroyAllWindows()