import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_eye.xml')
body_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_upperbody.xml')
lowbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_lowerbody.xml')
fullbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')
upbody_cascade = cv2.CascadeClassifier('..\haarcascade_upperbody.xml')
profile_cascade = cv2.CascadeClassifier('..\haarcascade_profileface.xml')
face2_cascade = cv2.CascadeClassifier('..\haarcascade_frontalface_alt_tree.xml')
hs_cascade = cv2.CascadeClassifier('HS.xml')
#img = cv2.imread(r'..\images\Capturar.png')
img = cv2.imread(r'..\images\rest_fila2.png')
#img = cv2.imread(r'..\images\person_032.bmp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
body = body_cascade.detectMultiScale(
    gray,
    minNeighbors = 2
)
for (xa, ya, wa, ha) in body:
    cv2.rectangle(img, (xa, ya), (xa+wa, ya+ha), (0, 255, 0), 2)

lbody = lowbody_cascade.detectMultiScale(
    gray,
    scaleFactor = 1.1,
    minNeighbors = 2
)
for (xb, yb, wb, hb) in lbody:
    cv2.rectangle(img, (xb, yb), (xb+wb, yb+hb), (255, 255, 0), 2)

fbody = fullbody_cascade.detectMultiScale(
    gray,
    scaleFactor = 1.1,
    minNeighbors = 2,
    flags = cv2.CASCADE_SCALE_IMAGE
)
for (xc, yc, wc, hc) in fbody:
    cv2.rectangle(img, (xc, yc), (xc+wc, yc+hc), (100, 255, 0), 2)
for (xd,yd,wd,hd) in faces:
    cv2.rectangle(img,(xd,yd),(xd+wd,yd+hd),(255,0,0),2)
    roi_gray = gray[yd:yd+hd, xd:xd+wd]
    roi_color = img[yd:yd+hd, xd:xd+wd]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
hs = hs_cascade.detectMultiScale(gray, minNeighbors = 2)
for (xe, ye, we, he) in hs:
        cv2.rectangle(img, (xe, ye), (xe+we, ye+he), (100, 100, 100), 2)
upb = upbody_cascade.detectMultiScale(gray, minNeighbors = 2)
for (xf, yf, wf, hf) in upb:
    cv2.rectangle(img, (xf, yf), (xf+wf, yf+hf), (10, 25, 255), 2) #vermelho

pfc = profile_cascade.detectMultiScale(gray, minNeighbors = 2)
for (xg, yg, wg, hg) in pfc:
    cv2.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255, 0, 255), 2) #rosa

face2 = face2_cascade.detectMultiScale(gray, minNeighbors = 2)
for (xh, yh, wh, hh) in pfc:
    cv2.rectangle(img, (xh, yh), (xh+wh, yh+hh), (255, 255, 0), 2) #

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()