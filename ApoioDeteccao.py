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
from CaracteristicasCalculadas import *
from Posicionamento import *



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

def Salvar_PontoAtualInterno(new_width, h, cnt, pid, new_x, y, cur):
    lista_objetos = []
    for i in range (new_width):
        for j in range (h):
            no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
            if (no_contorno>=0):
                x_salvar = new_x+i
                y_salvar = y+j
                if (no_contorno==0):
                    lista_objetos.append((None, 1, x_salvar,y_salvar, pid))
                if (no_contorno>0):
                    lista_objetos.append((None, 0, x_salvar,y_salvar, pid))
                j+=1
                i+=1
    cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?)", lista_objetos)
    return

def Adicionar_Pontos_Contorno(new_width, h, cnt, pessoax, new_x, y ,cur):
    lista_objetos = []
    for i in range (new_width):
        for j in range (h):
            no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
            x_salvar = new_x+i
            y_salvar = y+j
            if (no_contorno>=0):
                cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X = ? AND Y=? AND Pessoa_id=?""", (x_salvar, y_salvar, pessoax,))
                lista_ponto = cur.fetchall()
                if(len(lista_ponto)==0):
                    if (no_contorno==0):
                        lista_objetos.append((None, 1, x_salvar,y_salvar, pessoax))
                    if (no_contorno>0):
                        lista_objetos.append((None, 0, x_salvar,y_salvar, pessoax))
            j+=3
            i+=3
    cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?)", lista_objetos)
    return
                    