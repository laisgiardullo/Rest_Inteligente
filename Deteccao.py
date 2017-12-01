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
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'r')
    texto3 = arquivo3.readlines()
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'w')

    arquivo4 = open('resultados/res_numpy.txt', 'r')
    texto4 = arquivo4.readlines()
    arquivo4 = open('resultados/res_numpy.txt', 'w')

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

    arquivo3.writelines(texto3)
    arquivo3.close()
    arquivo4.writelines(texto4)
    arquivo4.close()



    return contours1


def Pessoa_Nova(cx, new_width, cy, cur, tempo_video):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (cx, cx, cy, cy,))
    quadrante = cur.fetchall()
    quadrante_id = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadrante_id=?""", (quadrante_id,))
    medida = (cur.fetchall())[0]
    xa = medida[1]
    ya = medida[2]
    limite = xa*xa+ya*ya
    cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X)+(?-Y)*(?-Y))<=? AND Atual=1 AND Instante_Inicial!=? ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y))""", (cx, cx, cy, cy, limite, tempo_video, cx, cx, cy, cy, ))
    
    #cur.execute("""SELECT * FROM 'Posicao' WHERE ((abs(?-X)<? OR abs(?-Y)<120) AND Atual=1) ORDER BY abs(?-X)""", (cx, new_width, cy, cx ))
    lista = cur.fetchall()
    print(len(lista))
    if (len(lista)>0):
        #print("eh velho")
        id_pessoa= lista[0][6]
        id_posicao=lista[0][0]
        novo = False
    else:
        novo = True
        id_pessoa= None
        id_posicao=None
    return (novo, id_pessoa, id_posicao)

def Determinar_Pessoa(contours1, img, areaTH, pid, num_frame, tempo_video, novos_pts, con, tipo_seguir):
     ### XX OUTROS TESTES XX ###
    #_, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ### XX OUTROS TESTES XX ###

    #num_contorno = 0
    #lista_width = []
    #texto4.append(str(contours1))
    #print (contours1)
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left

        largura_media = Largura_Media(x,y, cur)
        if (area>areaTH):
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            #lista_width.append(new_width)
            if(tipo_seguir == 1):
                pid = Salvar_Mostrar_PessoaMet1(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, con)
                novos_pts = []
            elif(tipo_seguir == 2):
                pid, novos_pts = Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, novos_pts,con)

    return img , pid, novos_pts




def Comparar_e_Salvar_Novos(contours1, img, areaTH, pid, num_frame, tempo_video, con):
    cur = con.cursor()
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left

        largura_media = Largura_Media(x,y, cur)
        if (area>areaTH):
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            it = 0 #it = iteracao
            lista_obj = []
            lista_obj_pos = []
            cur = con.cursor()
            for i in range (pp):
                novo = True
                new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)
                novo, pessoax, posicaox = Pessoa_Nova(cx, new_width, cy, cur, tempo_video)
                if (novo and cx>largura_padrao and cx<(w_frame-largura_padrao) and cy>altura_padrao and cy<(h_frame-altura_padrao)):
                    #print ("sounovo")
                    #p = Person.Pessoa_Pontual(pid,cx,cy, new_width, num_frame,tempo_video)
                    #(Id INT, X INT, Y INT, Status TEXT, Width INT, Num_Frame INT, Instante INT)")
                    #obj_pessoa = (Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)

                    lista_obj.append((pid,'in',new_width,tempo_video, None))
                    lista_obj_pos.append((None, cx, cy, tempo_video, None, 1, pid))
                    Salvar_PontoAtualInterno(new_width, h, cnt, pid, new_x, y, cur)
                    pid += 1
                    #########   EXPLICACAO LOGICA   ###########
                    ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
                    img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
                    it+=new_width
                    #pa = np.array ([[cx]])
                    #pb = np.array ([[cy]])
                    #nv_pt = np.dstack((pa,pb))
                    #nv_pt = nv_pt.astype(np.float32)
                    #if (num_frame>20): #so comeca a guardar depois do 21 que eh quando estabiliza o background
                    #    if (novos_pts !=[]):
                    #        novos_pts = np.append(novos_pts,nv_pt, axis = 0)
                    #    else: novos_pts = nv_pt
                else:
                    #Adicionar_Pontos_Contorno(new_width, h, cnt, pessoax, new_x, y ,cur)
                    pass
            if (lista_obj!=[]):
                with con:
                    cur = con.cursor()
                    cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
                    cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)

    return img , pid