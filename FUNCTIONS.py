#documento com funcoes utilizadas pelos metodos de deteccao

import numpy as np
import cv2
from autocanny import *
import Person
import time
import sqlite3 as lite

def Largura_Media(x, y):
    largura_media = 31
    return (largura_media)

def Qnt_Pessoas_Contorno (w, largura_media):
    pp = w//largura_media
    if (pp==0):
        pp=1
    return (pp)

def Atualizar_Retangulo(x, y, h, new_width, it):
    new_x = x+it #novo valor de x, caso seja mais de 1 pessoa 
    cx = new_x + (new_width/2) #cx = o centro do retangulo da pessoa, em x
    cy = y + (h/2) #cy = o centro do retangulo da pessoa, em y
    return (new_x, cx, cy)

def Aplicacao_Mascara(fgmask):
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    #########   EXPLICACAO LOGICA    ###########
    #Vamos aplicar a mascara 
    #########   EXPLICACAO FUNCAO   ###########
    #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
    #Adaptive thresholding: In this, the algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.
    #########   LINK   ###########
    #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    imBin = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY_INV,11,2)

    ### XX OUTROS TESTES XX ###
    #ret,imBin = cv2.threshold(fgmask,127,255,cv2.THRESH_BINARY)
    #imBin2 = cv2.adaptiveThreshold(teste2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #    cv2.THRESH_BINARY_INV,11,2)
    #Opening (erode->dilate) para tirar ruido.
    ### XX OUTROS TESTES XX ###

    mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)

    ### XX OUTROS TESTES XX ###
    #mask2 = cv2.morphologyEx(teste2, cv2.MORPH_OPEN, kernelOp)
    #Closing (dilate -> erode) para juntar regioes brancas.
    #mask2 =  cv2.morphologyEx(mask2 , cv2.MORPH_CLOSE, kernelCl)
    ### XX OUTROS TESTES XX ###

    mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    return (mask)

def Media_Pessoas_Frames(quantidade_frames_considerados, num_frame, persons):
    num_frame_maximo = num_frame - quantidade_frames_considerados # faco a media com os ultimos 8 frames
    num_pessoas_media = 0
    qnr_frames_inicio = 0
    if (num_frame_maximo<0): #se ainda nao passou da qnt de frames considerados (inicio do video), media de todos os anteriores
        for i in persons:
            num_pessoas_media+=1
        if (num_frame > 0):
            num_pessoas_media = num_pessoas_media/num_frame
    else:
        for i in persons:
            if (i.frame > num_frame_maximo):
                num_pessoas_media+=1
        num_pessoas_media = num_pessoas_media/quantidade_frames_considerados
    return (num_pessoas_media)

def Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, persons, num_frame,tempo_video, novos_pts, con):
    it = 0 #it = iteracao
    lista_obj = []
    lista_obj_pos = []
    for i in range (pp):
        novo = True
        new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)
        for ponto in range (len(novos_pts)):
            if((abs(cx-(novos_pts[ponto][0][0]))<new_width) and (abs(cy-(novos_pts[ponto][0][1]))<60)):
                novo = False
        if (novo):
            #print ("sounovo")
            #p = Person.Pessoa_Pontual(pid,cx,cy, new_width, num_frame,tempo_video)
            #(Id INT, X INT, Y INT, Status TEXT, Width INT, Num_Frame INT, Instante INT)")
            #obj_pessoa = (Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)

            lista_obj.append((pid,'in',new_width,tempo_video, None))
            lista_obj_pos.append((None, cx, cy, tempo_video, None, True, pid))
            #persons.append(p)
            pid += 1
            #########   EXPLICACAO LOGICA   ###########
            ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
            img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
            it+=new_width
            #lista_cx.append([cx])
            #lista_cy.append([cy])
            print("novospts:"+str(novos_pts))
            #print ("cx e cy"+str(cx)+str(cy))
            pa = np.array ([[cx]])
            pb = np.array ([[cy]])
            nv_pt = np.dstack((pa,pb))
            nv_pt = nv_pt.astype(np.float32)
            if (num_frame>20): #so comeca a guardar depois do 21 que eh quando estabiliza o background
                if (novos_pts !=[]):
                    novos_pts = np.append(novos_pts,nv_pt, axis = 0)
                else: novos_pts = nv_pt
    if (lista_obj!=[]):
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
            cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
    return (persons, pid, novos_pts)



def Imprimir_Novo_Objeto(texto, pid, cx, cy, num_contorno):
    ## XX EXCLUIR APOS TESTES XX ##
    print ("NOVO OBJETO")
    print ("ID:"+str(pid))
    print ("Cx:"+str(cx)+" Cy:"+str(cy))
    print ("Num Contorno:"+str(num_contorno))
    ## XX EXCLUIR APOS TESTES XX ##

    texto.append('\n \n NOVO OBJETO: ID '+str(pid))
    texto.append("\n Cx:"+str(cx)+" Cy:"+str(cy))
    texto.append("\n Num Contorno:"+str(num_contorno))
    texto.append('\n \n ')
    return(texto)

def Imprimir_ObjetoseTracks(texto, pessoas2, i):
    print (" ")
    print ("Pessoas:")
    print (pessoas2)
    print ("id:"+str(i.i))
    print(i.x)
    print(i.y)
    print (i.tracks)
    print (i.status)

    texto.append("\n Pessoas:"+str(pessoas2))
    texto.append('\n ID '+str(i.i))
    texto.append("\n (CX,CY) = ("+str(i.x)+","+str(i.y)+")")
    texto.append('\n Tracks: '+str(i.tracks))
    texto.append('\n Status '+str(i.status))
    texto.append(' \n \n')
    return(texto)