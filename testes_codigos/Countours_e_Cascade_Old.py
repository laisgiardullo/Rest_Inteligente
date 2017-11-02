import numpy as np
import cv2
from autocanny import *
#from matplotlib import pyplot as plt
body_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_upperbody.xml')
hs_cascade = cv2.CascadeClassifier('HS.xml')
cap = cv2.VideoCapture('videos\Refeitorio_Camera1.mp4') #Open video file
#cap = cv2.VideoCapture('videos\Estavel.mp4') #Open video file
cap.set(3,160) #set width (3) para 160
cap.set(4,90) #set height (4) para 160

fgbg = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=255, detectShadows=True)#Create the background substractor
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((9,9),np.uint8)
# areaTH=area minima para considerar uma pessoa
areaTH = 500
i=0
n_cont=0
while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    body = body_cascade.detectMultiScale(
    gray,
    minNeighbors = 2
    )
    for (x, y, w, h) in body:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    hs = hs_cascade.detectMultiScale(
    gray,
    minNeighbors = 2
    )
    for (x, y, w, h) in hs:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 10), 2)
    #i=i+1
    #if (i>30000):
    fgmask = fgbg.apply(frame) #Use the substractor
    teste2 = auto_canny(frame)
    #teste2 = cv2.Canny(frame, 100, 200)
    try:
        #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
        #Adaptive thresholding: In this, the algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.
        #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        #imBin = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #    cv2.THRESH_BINARY_INV,11,2)
        #imBin2 = cv2.adaptiveThreshold(teste2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #    cv2.THRESH_BINARY_INV,11,2)
        #Opening (erode->dilate) para tirar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(teste2, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regioes brancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        mask2 =  cv2.morphologyEx(mask2 , cv2.MORPH_CLOSE, kernelCl)
    except:
        #if there are no more frames to show...
        print('EOF')
        break
    #finding contours is like finding white object from black background. Object to be found should be white and background should be black.
    #cv2.RETR_EXTERNAL means we only care about external contours (contours within contours will not be detected) tentar RETR_TREE
    #cv2.CHAIN_APPROX_NONE is the algorithm used to make the contour
    #ver mais http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
    #ver hierarquia e contornos externos e internos em http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html
    _, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    __, contours1, hierarchy1 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours1:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 1, 8)
        area = cv2.contourArea(cnt)
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt)
        print area
        #if (area>500):
        if (area>500 and w>40 and w<140 and h>70 and h<180):
            #################
            #   TRACKING    #
            #################            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)            
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            textw = "Width " + str(w)
            texth = "Height " + str(h)

        # #cv.PutText(img, text, org, font, color) -  where org is the origin (bottom-left corner) of the text to write.
            cv2.putText(frame, textw ,(x,y),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame, texth ,(x,y+20),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow('Frame',frame)

    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows