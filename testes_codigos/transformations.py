import cv2
import numpy as np

img = cv2.imread("noise.png")
#threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
#ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

#matriz cheia de uns, com 3 linhas e 3 colunas, tipo de dado np.uint8; quanto maior a matriz, "maior o pixel" transformado
#ver https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.ones.html
kernel = np.ones((3,3),np.uint8)

#ver http://docs.opencv.org/2.4/doc/tutorials/imgproc/erosion_dilatation/erosion_dilatation.html
erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(img,kernel,iterations = 1)

cv2.imwrite("erode.png",erosion)
cv2.imwrite("dilate.png",dilation)