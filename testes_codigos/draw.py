import numpy as np
import cv2

cap = cv2.VideoCapture('peopleCounter.avi') #Open video file

# ##PARA MOSTRAR PROPRIEDADES:

# for i in range(19):
#     print i, cap.get(i)

# ##para fixar altura e largura:
# cap.set(3,160) #set width
# cap.set(4,120) #set height

w = cap.get(3) #get width
h = cap.get(4) #get height

mx = int(w/2)
my = int(h/2)

count = 0

while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    try:
        # ##PARA ESCREVER:
        # count = count + 1
        # text = "Hello World " + str(count)
        # #cv.PutText(img, text, org, font, color) -  where org is the origin (bottom-left corner) of the text to write.
        # cv2.putText(frame, text ,(mx,my),cv2.FONT_HERSHEY_SIMPLEX
        #             ,1,(255,255,255),1,cv2.LINE_AA)

        ## PARA DESENHAR:
        frame2 = frame

        cv2.imshow('Frame',frame)
    except:
        #if there are no more frames to show...
        print('EOF')
        break

## PARA DESENHAR:
#numpy.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
    line1 = np.array([[100,100],[300,100],[350,200]], np.int32).reshape((-1,1,2))
    line2 = np.array([[400,50],[450,300]], np.int32).reshape((-1,1,2))

#In order for polylines to work, it needs to receive a numpy array with the coordinate pairs (x and y) for each point in the line, in our case, beginning and end. If you want to specify the points like I did, you also need to call reshape(-1,1,2) for it to work with polylines().
    #cv2.polylines(img, pts, isClosed, color[, thickness[, lineType[, shift]]])
    frame2 = cv2.polylines(frame2,[line1],False,(255,0,0),thickness=2)
    frame2 = cv2.polylines(frame2,[line2],False,(0,0,255),thickness=1)
    
    cv2.imshow('Frame 2',frame2)

    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows