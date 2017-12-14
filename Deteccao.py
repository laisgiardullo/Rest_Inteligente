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
from ApoioDeteccao import *
from CaracteristicasCalculadas import *
from Posicionamento import *


def Countours_Area_Pontual(img, fgbg, persons, pid, num_frame, tempo_video, novos_pts, con):
    #arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'r')
    #texto3 = arquivo3.readlines()
    #arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'w')

    #arquivo4 = open('resultados/res_numpy.txt', 'r')
    #texto4 = arquivo4.readlines()
    #arquivo4 = open('resultados/res_numpy.txt', 'w')

    #inicializacao de variaveis
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    #areaTH = 100 # areaTH=area minima para considerar uma pessoa
    #quantidade_frames_considerados = 8

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

    #num_contorno = 0
    #lista_width = []
    #texto4.append(str(contours1))
    #print (contours1)

    #arquivo3.writelines(texto3)
    #arquivo3.close()
    #arquivo4.writelines(texto4)
    #arquivo4.close()



    return contours1




def Pessoa_Nova_new(new_width, h, cnt, pid, new_x, y, cur, lista_pontosinternos, limitex, limitey):
    print("pessoa novanew")
    lista_objetos = lista_pontosinternos
    novo = True
    #lista_pontos = []

    id_pessoa = None
    max_x = new_x+new_width
    max_y = y+h
    centro_x = new_x+new_width/2
    centro_y = y+h/2
    lista_pessoas = []
    ignorar = False

    cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X<=? AND X>=? AND Y<=? AND Y>=?""", (max_x,new_x, max_y,y,))
    lista_pontos = cur.fetchall()
    if (len(lista_pontos)!=0):
        novo = False
        for pto in lista_pontos:
            lista_pessoas.append(pto[4])
        lista_sem_duplicatas = list(set(lista_pessoas))
        print("listasem "+str(lista_sem_duplicatas))
        total_pessoas = len(lista_sem_duplicatas)
        if (total_pessoas == 1):
            id_pessoa = lista_pessoas[0]
            print("idpessoa"+str(id_pessoa))
        elif (total_pessoas>1):
            ignorar = True
    else:
        cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X))<=? AND ((?-Y)*(?-Y))<=? AND Atual=1 ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y)) ASC""", (centro_x, centro_x, limitex, centro_y, centro_y, limitey, centro_x, centro_x, centro_y, centro_y, ))
        lista_posicoesprox = cur.fetchall()
        #if (len(lista_posicoesprox)>0):
        #    id_pessoa = lista_posicoesprox[0][6]
        #    novo = False
        if (len(lista_posicoesprox)==1):
            novo = False
            id_pessoa = lista_posicoesprox[0][6]
        elif (len(lista_posicoesprox)>1):
            ignorar = True
            novo = False
    #achou_proximo = False
    if (ignorar == False):
        i=0
        j=0
        while (i < new_width):
            while (j< h):
                #achou_existente = False
                no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
                
                if (no_contorno>0): #se estiver dentro do contorno
                    
                    x_salvar = new_x+i
                    y_salvar = y+j
                    cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X-1<? AND X+1>? AND Y-1<? AND Y+1>?""", (x_salvar,x_salvar,y_salvar,y_salvar))
                    lista_pontos_salvos = cur.fetchall()
                    if (len(lista_pontos_salvos)==0):
                        if (novo):
                            #cur.execute("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", (None, 0, x_salvar,y_salvar, pid, None))
                            lista_objetos.append([None, 0, x_salvar,y_salvar, pid, None])
                        else:
                            lista_objetos.append([None, 0, x_salvar,y_salvar, id_pessoa, None])
                            #cur.execute("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", (None, 0, x_salvar,y_salvar, id_pessoa, None))
                j+=8
            j=0
            i+=8


    #cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?)", lista_objetos)
    return (novo, id_pessoa, lista_objetos)



def Comparar_e_Salvar_Novos2(contours1, img, areaTH, pid, num_frame, tempo_video, con):
    cur = con.cursor()
    lista_pontosinternos = []
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left

        largura_media, altura_media = Medidas_Media(x+w/2,y+h/2, cur)
        areaTH = largura_media*altura_media/3
        limitex = largura_media*largura_media
        limitey = altura_media*altura_media
        if (area>areaTH):
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            it = 0 #it = iteracao
            lista_obj = []
            lista_obj_pos = []
            
            for i in range (pp):
                novo = True
                new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)
                novo, pessoax, lista_pontosinternos = Pessoa_Nova_new(new_width, h, cnt, pid, new_x, y, cur, lista_pontosinternos, limitex, limitey)
                #novo, pessoax, posicaox = Pessoa_Nova(cx, new_width, cy, cur, tempo_video)
                it+=new_width
                if (novo):
                #if (novo and cx>largura_padrao and cx<(w_frame-largura_padrao) and cy>altura_padrao and cy<(h_frame-altura_padrao)):
                    lista_obj.append((pid,'in',new_width,tempo_video, None))
                    lista_obj_pos.append((None, cx, cy, tempo_video, None, 1, pid))
                    pid += 1
                    #########   EXPLICACAO LOGICA   ###########
                    ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
                    img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
                    
            if (lista_obj!=[]):
                #with con:
                    #cur = con.cursor()
                cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
                cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
                cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", lista_pontosinternos)
                lista_obj=[]
                lista_obj_pos=[]
                lista_pontosinternos = []
                    #else:
                        #Adicionar_Pontos_Contorno(new_width, h, cnt, pessoax, new_x, y ,cur)

    if (lista_pontosinternos!=[]):
        cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", lista_pontosinternos)
        lista_pontosinternos = []

    return img , pid

