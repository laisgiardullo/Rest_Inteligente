import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_eye.xml')
body_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_upperbody.xml')
lowbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_lowerbody.xml')
fullbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')
img = cv2.imread('..\images\Rest1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
body = body_cascade.detectMultiScale(
    gray,
    minNeighbors = 2
)
for (x, y, w, h) in body:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

lbody = lowbody_cascade.detectMultiScale(
    gray,
    scaleFactor = 1.1,
    minNeighbors = 2
)
for (x, y, w, h) in lbody:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

fbody = fullbody_cascade.detectMultiScale(
    gray,
    scaleFactor = 1.1,
    minNeighbors = 2,
    flags = cv2.CASCADE_SCALE_IMAGE
)
for (x, y, w, h) in fbody:
    cv2.rectangle(img, (x, y), (x+w, y+h), (100, 255, 0), 2)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()