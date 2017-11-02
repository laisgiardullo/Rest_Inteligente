import numpy as np
import cv2
import autocanny

cap = cv2.VideoCapture('videos\Estavel.mp4') #Open video file
cap.set(3,160) #set width (3) para 160
cap.set(4,90) #set height (4) para 160

fgbg = cv2.createBackgroundSubtractorMOG2(history=1500, varThreshold=255, detectShadows=True)#Create the background substractor
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((9,9),np.uint8)
# areaTH=area minima para considerar uma pessoa
areaTH = 500
i=0
n_cont=0
while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    #i=i+1
    #if (i>30000):
    fgmask = fgbg.apply(frame) #Use the substractor
    try:
        #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
        #Adaptive thresholding: In this, the algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.
        #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        imBin = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,11,2)
        #Opening (erode->dilate) para tirar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regioes brancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    except:
        #if there are no more frames to show...
        print('EOF')
        break
    #finding contours is like finding white object from black background. Object to be found should be white and background should be black.
    #cv2.RETR_EXTERNAL means we only care about external contours (contours within contours will not be detected)
    #cv2.CHAIN_APPROX_NONE is the algorithm used to make the contour
    #ver mais http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)
        #x,y,w,h = cv2.boundingRect(cnt)
        print area
        if area > areaTH:
            #################
            #   TRACKING    #
            #################            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)            
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            textw = "Width " + str(w)
            texth = "height " + str(h)

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