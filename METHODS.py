#Documento com funcoes de metodos utilizados para deteccao

#ver https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.ndarray.html para numpy e https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.dtype.html
import numpy as np
import cv2
import math
from autocanny import *
import Person
import time
from FUNCTIONS import *
import sqlite3 as lite
import sys


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

def Countours_Area(img, fgbg, persons, pid, max_p_age, nframe, tempo_video):
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

    num_pessoas = 0
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    areaTH = 100 # areaTH=area minima para considerar uma pessoa
    i=0
    n_cont=0
    fgmask = fgbg.apply(img) #Use the substractor: aqui, o fundo, que nao esta mexendo, fica preto e o que esta se movimentando branco
    cv2.imshow('fgmask',fgmask)
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
        if (area>areaTH):

            num_contorno+=1

            pp = w//31
            if (pp==0): pp=1
            num_pessoas = num_pessoas + pp

        ### XX OUTROS TESTES XX ###
        #if (area>500 and w>40 and w<140 and h>70 and h<180):
        ### XX OUTROS TESTES XX ###

            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            it = 0 #it = iteracao
            for i in range (pp):
                new_x = x+it #novo valor de x, caso seja mais de 1 pessoa 
                new = True #new = nova pessoa
                cx = new_x + (new_width/2) #cx = o centro do retangulo da pessoa, em x
                cy = y + (h/2) #cy = o centro do retangulo da pessoa, em y

                #########   EXPLICACAO LOGICA    ###########
                #Agora vamos percorrer todos os objetos da classe MyPerson e compara-los com o contorno em questao
                for i in persons:
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

                        #if ((cx >= (i.x - (i.width/2))) and (cx <= (i.x + (i.width/2)))):self, xn, yn, nframe, instante
                            new = False
                            i.updateCoords(cx,cy, nframe, tempo_video)   #actualiza coordenadas en el objeto and resets age
                            if (new_x < 150): i.setOut() #se ele passou pela porta de saida


                            ## XX EXCLUIR APOS TESTES XX ##
                            #print ("aqui false")
                            #print (new)
                            #print (i.i)
                            ## XX EXCLUIR APOS TESTES XX ##
                        elif ((i.getX() >= (new_x) and i.getX() <= (new_x + new_width))):
                            new = False
                            i.updateCoords(cx,cy, nframe, tempo_video)   #actualiza coordenadas en el objeto and resets age
                            if (new_x < 150): i.setOut() #se ele passou pela porta de saida

                #########   EXPLICACAO LOGICA   ###########
                #Se ele nao achou nenhum objeto antigo com coordenadas parecidas, new vai continuar True e eu preciso criar um novo objeto
                if (new == True):

                    ## XX EXCLUIR APOS TESTES XX ##
                    #print ("NOVO OBJETO")
                    #print ("ID:"+str(pid))
                    #print ("Cx:"+str(cx)+" Cy:"+str(cy))
                    #print ("Num Contorno:"+str(num_contorno))
                    ## XX EXCLUIR APOS TESTES XX ##

                    texto.append('\n \n NOVO OBJETO: ID '+str(pid))
                    texto.append("\n Cx:"+str(cx)+" Cy:"+str(cy))
                    texto.append("\n Num Contorno:"+str(num_contorno))
                    texto.append('\n \n ')


                    #########   EXPLICACAO FUNCAO   ###########
                    #pid = id, cx = centro x, cy = centro y, max_p_age = idade maxima, "in" = status (dentro do restaurante)
                    #self, i, xi, yi, max_age, status, width, num_frame, instante
                    p = Person.MyPerson(pid,cx,cy, max_p_age, "in", new_width, nframe,tempo_video)
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
    texto.append('\n \n TOTAL DE OBJETOS')
    texto.append('\n \n ')
    for i in persons:
        print(i.status)
        if (i.status == "in"):
            if ((nframe - i.ultimo_frame)>4):
                i.setOff()
            else:

                ## XX EXCLUIR APOS TESTES XX ##
                #print (" ")
                #print ("Pessoas:")
                #print (pessoas2)
                #print ("id:"+str(i.i))
                #print(i.x)
                #print(i.y)
                #print (i.tracks)
                #print (i.status)

                texto.append("\n Pessoas:"+str(pessoas2))
                texto.append('\n ID '+str(i.i))
                texto.append("\n (CX,CY) = ("+str(i.x)+","+str(i.y)+")")
                texto.append('\n Tracks: '+str(i.tracks))
                texto.append('\n Status '+str(i.status))
                texto.append(' \n \n')

                ## XX EXCLUIR APOS TESTES XX ##
                #cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
                cv2.circle(img,(i.getX(),i.getY()), 5, (0,0,255), 10) #desenho a bolinha vermelha
                pessoas2=pessoas2+1 #somo ao contador de pessoas

    ## XX EXCLUIR APOS TESTES XX ##
    print("PessoasTot"+str(pessoas2))
    print (num_pessoas)
    print ("pid"+str(pid))
    texto.append('\n \n\n \n FIM DO FRAMEEEEE\n \n\n \n')

    ## XX EXCLUIR APOS TESTES XX ##

    texto2.append('\n Total pessoas: '+str(pessoas2))
    texto2.append('\n Total IDs: '+str(pid))
    texto2.append('\n Total Deteccoes: '+str(num_pessoas))
    tempo_segundos = tempo_video/1000
    tempo_minutos = tempo_segundos//60
    tempo_segundos = tempo_segundos - tempo_minutos*60
    tempo_horas = tempo_minutos//60
    tempo_minutos = tempo_minutos - tempo_horas*60

    string_tempo = str(tempo_horas) + ":"+str(tempo_minutos)+":"+str(tempo_segundos)

    texto3.append(str(num_pessoas)+";"+str(pessoas2)+";"+str(pid)+";"+string_tempo+"\n")

    arquivo.writelines(texto)
    arquivo.close()
    arquivo2.writelines(texto2)
    arquivo2.close()
    arquivo3.writelines(texto3)
    arquivo3.close()


    return img , persons, pid

def Countours_Area_Door(img, fgbg, persons, pid, max_p_age, nframe, tempo_video):
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
        largura_media = Largura_Media(x,y)
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

#media frames:
def Countours_Area_Pontual(img, fgbg, persons, pid, max_p_age, num_frame, tempo_video, novos_pts, con):
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'r')
    texto3 = arquivo3.readlines()
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'w')

    arquivo4 = open('resultados/res_numpy.txt', 'r')
    texto4 = arquivo4.readlines()
    arquivo4 = open('resultados/res_numpy.txt', 'w')

    #inicializacao de variaveis
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    areaTH = 100 # areaTH=area minima para considerar uma pessoa
    quantidade_frames_considerados = 8

    #Inicializacao de contadores
    num_pessoas = 0
    i=0
    n_cont=0

    #Aplicacao do substractor
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
    lista_width = []
    #texto4.append(str(contours1))
    #print (contours1)
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left
        largura_media = Largura_Media(x,y)
        if (area>areaTH):
            num_contorno+=1
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            num_pessoas = num_pessoas + pp
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            #lista_width.append(new_width)
            persons, pid, novos_pts = Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, persons, num_frame,tempo_video, novos_pts,con)

                ### XX OUTROS TESTES XX ###
                #cv2.circle(img,(cx,cy), 5, (0,0,255), -1)           
                #textw = "Width " + str(new_width)
                #texth = "Height " + str(h)
                ### XX OUTROS TESTES XX ###
    
    #########   EXPLICACAO LOGICA   ###########
    #Agora, vou percorrer todos os objetos de pessoas salvos e calcular o numero aproximado de pessoas baseado na media anterior
    #con.commit()
    num_pessoas_media = Media_Pessoas_Frames(quantidade_frames_considerados, num_frame, persons)
 
    texto3.append(str(num_pessoas)+";"+str(num_pessoas_media)+";"+str(tempo_video)+"\n")

    arquivo3.writelines(texto3)
    arquivo3.close()
    arquivo4.writelines(texto4)
    arquivo4.close()



    return img , persons, pid, novos_pts

def OptFlow(old_frame, frame, p0, mask):
            #fonte: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
     
    # Create some random colors
    #color = np.random.randint(0,255,(100,3))
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    print("p1: "+str(p1))

     # Select good points
    #good_new = p1[st==1] #status==1: flow foi encontrado
    #good_old = p0[st==1]
    #print("good_new:"+str(good_new))
    #print("good_old:"+str(good_new))
    # # draw the tracks

    # #ZIP x = [1, 2, 3], y = [4, 5, 6], zip(x, y) =[(1, 4), (2, 5), (3, 6)]
    # #ENUMERATE seasons = ['Spring', 'Summer', 'Fall', 'Winter'], list(enumerate(seasons)) = [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
    # # i = numero do enumerate, new = elemento do good_new, old = elemento do good_old
    # for i,(new,old) in enumerate(zip(good_new,good_old)):
    for i,(new,old) in enumerate(zip(p1,p0)):
        a,b = new.ravel() #ravel: A 1-D array, containing the elements of the input, is returned
        c,d = old.ravel()
        #if((a,b)!=(c,d)):
        mask = cv2.line(mask, (a,b),(c,d), (0,255,0), 2)
        frame = cv2.circle(frame,(a,b),5,(0,255,0),-1)

    img = cv2.add(frame,mask)

    cv2.imshow('frame_22',img)

    # # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    # #p0 = good_new.reshape(-1,1,2)
    #if(len(good_new)==len(p1)):
    #    try:
    #        print("gnr:"+str(good_new.reshape(-1,1,2)))
    #        good_new = good_new.reshape(-1,1,2) #voltar ao formato original de p0
    #        novos_pts = good_new
    #    except:
    #        pass
    novos_pts = p1
    return (novos_pts, mask)