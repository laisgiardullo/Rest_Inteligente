import numpy as np
import cv2

cap = cv2.VideoCapture('videos\Fila_Camera1.mp4') #Open video file

# alternativa: fgbg = cv2.createBackgroundSubtractorKNN() 
#history: quanto tempo ele "segura" o detectado. varThreshold: granularidade
fgbg = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=255, detectShadows=True) #Create the background object

while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    
    fgmask = fgbg.apply(frame) #Use the substractor 

    #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
    #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    ret,thresh1 = cv2.threshold(fgmask,127,255,cv2.THRESH_BINARY)
    #thresh1 = cv2.Canny(fgmask, 225, 250)

    #thresh1 = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #        cv2.THRESH_BINARY_INV,11,2)
    #matriz cheia de uns, com 3 linhas e 3 colunas, tipo de dado np.uint8; quanto maior a matriz, "maior o pixel" transformado
    #ver https://docs.scipy.org/doc/numpy-1.10.1/reference/ge1nerated/numpy.ones.html
    kernel = np.ones((3,3),np.uint8)

    #ver http://docs.opencv.org/2.4/doc/tutorials/imgproc/erosion_dilatation/erosion_dilatation.html
    fgmask = cv2.dilate(fgmask,kernel,iterations = 1)
    fgmask = cv2.erode(fgmask,kernel,iterations = 1)
    
    
    try:        
        cv2.imshow('Frame',frame)
        cv2.imshow('Background Substraction',fgmask)
    except:
        #if there are no more frames to show...
        print('EOF')
        break
    
    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows