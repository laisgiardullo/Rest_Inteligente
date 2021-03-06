#Documento com funcoes de metodos utilizados para deteccao

#ver https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.ndarray.html para numpy e https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.dtype.html
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
from Posicionamento import *


def Cascade1 (img):
    face_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_eye.xml')
    body_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_upperbody.xml')
    lowbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_lowerbody.xml')
    fullbody_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')
    upbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    face2_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')
    hs_cascade = cv2.CascadeClassifier('HS.xml')
    #img = cv2.imread(r'..\images\Capturar.png')
    img = cv2.imread(r'images\rest_fila2.png')
    #img = cv2.imread(r'..\images\person_032.bmp')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    body = body_cascade.detectMultiScale(
        gray,
        minNeighbors = 2
    )
    for (xa, ya, wa, ha) in body:
        cv2.rectangle(img, (xa, ya), (xa+wa, ya+ha), (0, 255, 0), 2)
        cv2.putText(img, "body" ,(xa,ya),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    lbody = lowbody_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 2
    )
    for (xb, yb, wb, hb) in lbody:
        cv2.rectangle(img, (xb, yb), (xb+wb, yb+hb), (255, 255, 0), 2)
        cv2.putText(img, "lbody" ,(xb,yb),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)

    fbody = fullbody_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 2,
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    for (xc, yc, wc, hc) in fbody:
        cv2.rectangle(img, (xc, yc), (xc+wc, yc+hc), (100, 255, 0), 2)
        cv2.putText(img, "fbody" ,(xe,ye),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    for (xd,yd,wd,hd) in faces:
        cv2.rectangle(img,(xd,yd),(xd+wd,yd+hd),(255,0,0),2)
        roi_gray = gray[yd:yd+hd, xd:xd+wd]
        roi_color = img[yd:yd+hd, xd:xd+wd]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        cv2.putText(img, "faces" ,(xd,yd),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    hs = hs_cascade.detectMultiScale(gray, minNeighbors = 2)
    for (xe, ye, we, he) in hs:
            cv2.rectangle(img, (xe, ye), (xe+we, ye+he), (100, 100, 100), 2)
            cv2.putText(img, "HS" ,(xe,ye),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    upb = upbody_cascade.detectMultiScale(gray, minNeighbors = 2)
    for (xf, yf, wf, hf) in upb:
        cv2.rectangle(img, (xf, yf), (xf+wf, yf+hf), (10, 25, 255), 2) #vermelho
        cv2.putText(img, "UPB" ,(xf,yf),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    pfc = profile_cascade.detectMultiScale(gray, minNeighbors = 2)
    for (xg, yg, wg, hg) in pfc:
        cv2.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255, 0, 255), 2) #rosa
        cv2.putText(img, "pfc" ,(xg,yg),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    face2 = face2_cascade.detectMultiScale(gray, minNeighbors = 2)
    
    return img

def Cascade (img):
    body_cascade = cv2.CascadeClassifier('\Users\Lais\Downloads\opencv\sources\data\haarcascades\haarcascade_upperbody.xml')
    #hs = heads and shoulders, fonte http://alereimondo.no-ip.org/OpenCV/36
    #http://alereimondo.no-ip.org/OpenCV/34.version?id=60
    hs_cascade = cv2.CascadeClassifier('HS.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    body = body_cascade.detectMultiScale(gray, minNeighbors = 2)
    hs = hs_cascade.detectMultiScale(gray, minNeighbors = 2)
    for (x, y, w, h) in body:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x, y, w, h) in hs:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 10), 2)
    return img
    
def Countours (img, fgbg):
    #fgbg = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=255, detectShadows=True)#Create the background substractor
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((9,9),np.uint8)
    # areaTH=area minima para considerar uma pessoa
    areaTH = 500
    i=0
    n_cont=0
    fgmask = fgbg.apply(img) #Use the substractor
    teste2 = auto_canny(img)
    #teste2 = cv2.Canny(img, 100, 200)
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
    #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
    #Adaptive thresholding: In this, the algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.
    #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        #imBin = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #    cv2.THRESH_BINARY_INV,11,2)
        #imBin2 = cv2.adaptiveThreshold(teste2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #    cv2.THRESH_BINARY_INV,11,2)
        #Opening (erode->dilate) para tirar ruido.
        #https://docs.opencv.org/2.4/doc/tutorials/imgproc/opening_closing_hats/opening_closing_hats.html
        #https://docs.opencv.org/2.4/doc/tutorials/imgproc/erosion_dilatation/erosion_dilatation.html
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(teste2, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regioes brancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        mask2 =  cv2.morphologyEx(mask2 , cv2.MORPH_CLOSE, kernelCl)
    except:
        #if there are no more imgs to show...
        print('EOF')
    #finding contours is like finding white object from black background. Object to be found should be white and background should be black.
    #cv2.RETR_EXTERNAL means we only care about external contours (contours within contours will not be detected) tentar RETR_TREE
    #cv2.CHAIN_APPROX_NONE is the algorithm used to make the contour
    #ver mais http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
    #ver hierarquia e contornos externos e internos em http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html
    _, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    __, contours1, hierarchy1 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 1, 8)
        area = cv2.contourArea(cnt)
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt)
        if (area>200):
        #if (area>500 and w>40 and w<140 and h>70 and h<180):
            #################
            #   TRACKING    #
            #################            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(img,(cx,cy), 5, (0,0,255), -1)            
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            textw = "Width " + str(w)
            texth = "Height " + str(h)

        # #cv.PutText(img, text, org, font, color) -  where org is the origin (bottom-left corner) of the text to write.
            cv2.putText(img, textw ,(x,y),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(img, texth ,(x,y+20),cv2.FONT_HERSHEY_SIMPLEX
                     ,1,(255,255,255),1,cv2.LINE_AA)
    return img


def Countours_Area_Door(img, fgbg, persons, pid, nframe, tempo_video):
    #arquivos de texto para controle
    arquivo = open('resultados/resultado_testes.txt', 'r')
    texto = arquivo.readlines()
    arquivo2 = open('resultados/resultado_testes_frame.txt', 'r')
    texto2 = arquivo2.readlines()
    arquivo3 = open('resultados/resultado_testes_frame_excel.txt', 'r')
    texto3 = arquivo3.readlines()

    texto.append('\n \n -------------------------------------------------------INICIO TESTE')
    texto2.append('\n \n ------FRAME: '+str(nframe))
    arquivo = open('resultados/resultado_testes.txt', 'w')
    arquivo2 = open('resultados/resultado_testes_frame.txt', 'w')
    arquivo3 = open('resultados/resultado_testes_frame_excel.txt', 'w')

    #inicializacao de variaveis
    line2 = np.array([[200,500], [5,100]], np.int32).reshape((-1,1,2))
    img = cv2.polylines(img,[line2],False,(0,0,255),thickness=1)
    areaTH = 100 # areaTH=area minima para considerar uma pessoa

    #inicializacao de contadores
    num_pessoas = 0
    i=0
    n_cont=0

    fgmask = fgbg.apply(img) #Use the substractor: aqui, o fundo, que nao esta mexendo, fica preto e o que esta se movimentando branco
    try:
        mask = Aplicacao_Mascara(fgmask)

    except:
        #se nao tem mais imagens para mostrar...
        print('EOF')

    #finding contours is like finding white object from black background. Object to be found should be white and background should be black.
    #cv2.RETR_EXTERNAL means we only care about external contours (contours within contours will not be detected) tentar RETR_TREE
    #cv2.CHAIN_APPROX_NONE is the algorithm used to make the contour
    #########   LINK   ###########
    #ver mais http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
    #ver hierarquia e contornos externos e internos em http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html

    __, contours1, hierarchy1 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    ### XX OUTROS TESTES XX ###
    #_, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ### XX OUTROS TESTES XX ###

    num_contorno = 0

    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left
        largura_media = Largura_Media(x,y, cur)
        if (area>areaTH):

            num_contorno+=1

            pp = Qnt_Pessoas_Contorno(w, largura_media)
            num_pessoas = num_pessoas + pp

        ### XX OUTROS TESTES XX ###
        #if (area>500 and w>40 and w<140 and h>70 and h<180):
        ### XX OUTROS TESTES XX ###

            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            it = 0 #it = iteracao
            for i in range (pp):
                new = True #new = nova pessoa
                new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)

                #########   EXPLICACAO LOGICA    ###########
                #Agora vamos percorrer todos os objetos da classe MyPerson e compara-los com o contorno em questao
                for i in persons:
                    print(i.status)
                    if (i.status == "in"):
                        ### XX OUTROS TESTES XX ###
                        #print (i.getX())
                        #print("NOVOX"+str(new_x)+"WIDTH"+str(new_width))
                        #if abs(cx-i.getX()) <= new_width and abs(cy-i.getY()) <= h:
                        #if abs(new_x-i.getX()) <= new_width and abs(y-i.getY()) <= h:
                        ### XX OUTROS TESTES XX ###

                        #########   EXPLICACAO LOGICA    ###########
                        # novo retangulo tem vertices em x = new_x e em x= (new_x + new_width)
                        # se antigo centro (do objeto i em persons) estiver dentro retangulo novo.. Ainda e o mesmo objeto e so atualizamos seu novo centro
                        if (i.getX() >= (new_x) and i.getX() <= (new_x + new_width)):
                        #dist = math.sqrt((cx - i.getX())**2 + (cy - i.getY())**2)
                        #if (dist <= w/2 and dist <= h/2):
                        #if ((cx >= (i.x - (i.width/2))) and (cx <= (i.x + (i.width/2)))):
                            new = False
                            i.updateCoords(cx,cy, nframe, tempo_video)   #actualiza coordenadas en el objeto and resets age
                        #    if (new_x < 150): i.setOut() #se ele passou pela porta de saida


                        #elif ((i.getX() >= (new_x) and i.getX() <= (new_x + new_width))):
                        #    new = False
                        #    i.updateCoords(cx,cy, nframe, tempo_video)   #actualiza coordenadas en el objeto and resets age
                        #    if (new_x < 150): i.setOut() #se ele passou pela porta de saida

                #########   EXPLICACAO LOGICA   ###########
                #Se ele nao achou nenhum objeto antigo com coordenadas parecidas, new vai continuar True e eu preciso criar um novo objeto
                if (new == True):
                    #[200,500], [5,100]]
                    if True:
                    #if (cx >=5 and cx<=200 and cy<=500 and cy>=100):

                        #########   EXPLICACAO FUNCAO   ###########
                        #pid = id, cx = centro x, cy = centro y, max_p_age = idade maxima, "in" = status (dentro do restaurante)
                        p = Person.MyPerson(pid,cx,cy, max_p_age, "in", new_width, nframe, tempo_video)
                        persons.append(p)
                        pid += 1

                    #########   EXPLICACAO LOGICA   ###########
                    ##agora, vamos fazer um teste: desenhar retangulo para comparar com as bolinhas
                    img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)

                    ### XX OUTROS TESTES XX ###
                    #cv2.circle(img,(cx,cy), 5, (0,0,255), -1)           
                    #textw = "Width " + str(new_width)
                    #texth = "Height " + str(h)
                    ### XX OUTROS TESTES XX ###

                    it = it + new_width #somo a iteracao a nova largura, para desenho da proxima pessoa no mesmo contorno (grupo)
    
    #########   EXPLICACAO LOGICA   ###########
    #Agora, vou percorrer todos os objetos de pessoas salvos e desenhar uma bolinha vermelha nos que estao no restaurante (status == "in")
    pessoas2 = 0 #contador de pessoas
    #texto.append('\n \n TOTAL DE OBJETOS')
    #texto.append('\n \n ')
    for i in persons:
        if (i.status == "in"):
            #cada segundo-> tempo_video = 1000
            if ((tempo_video - i.ultimo_instante)>1000):
                i.setOff()
            else:
                #texto = Imprimir_ObjetoseTracks(texto, pessoas2, i)
                cv2.circle(img,(i.getX(),i.getY()), 5, (0,0,255), -1) #desenho a bolinha vermelha
                pessoas2=pessoas2+1 #somo ao contador de pessoas
    cv2.putText(img, str(tempo_video) ,(50,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)

    ## XX EXCLUIR APOS TESTES XX ##
    #texto.append('\n \n\n \n FIM DO FRAMEEEEE\n \n\n \n')
    ## XX EXCLUIR APOS TESTES XX ##

    texto2.append('\n Total pessoas: '+str(pessoas2))
    texto2.append('\n Total IDs: '+str(pid))
    texto2.append('\n Total Deteccoes: '+str(num_pessoas))

    texto3.append(str(num_pessoas)+";"+str(pessoas2)+";"+str(pid)+";"+str(tempo_video)+"\n")

    arquivo.writelines(texto)
    arquivo.close()
    arquivo2.writelines(texto2)
    arquivo2.close()
    arquivo3.writelines(texto3)
    arquivo3.close()


    return img , persons, pid

