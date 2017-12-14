import numpy as np
import cv2
#from autocanny import *
from METHODS import *
import Person
import time
import sqlite3 as lite
import sys

from variaveis_globais import * #w_frame etc aqui
from Deteccao import *
from ApoioDeteccao import *
from CaracteristicasCalculadas import *
from Posicionamento import *

def Inicializar_Pixel(cur):
	lista_pixels=[]
	for x in range (w_frame):
		for y in range (h_frame):
			lista_pixels.append((None,x,y))
	cur.executemany("""INSERT INTO Pixel VALUES (?,?,?)""", lista_pixels)
	return

def Inicializar_Quadrantes(cur):
    largura_quad = w_frame/raiz_n_quad
    altura_quad = h_frame/raiz_n_quad
    for i in range (raiz_n_quad):
        for j in range(raiz_n_quad):
            valores_input = (None, i, j,largura_quad*i, altura_quad*j, largura_quad, altura_quad, largura_padrao, altura_padrao)
            cur.execute("""INSERT INTO Quadrantes VALUES (?,?,?,?,?,?,?,?,?)""", valores_input)
    return

def Media_Medidas(lista_medidas):
    largura = 0
    altura = 0
    for medida in lista_medidas:
        largura+=medida[3]
        altura+=medida[4]
    largura=largura/len(lista_medidas)
    altura=altura/len(lista_medidas)
    return largura, altura

def TotalMedidaFinal(cur):
    cur.execute("""SELECT * FROM 'MedidaParcial'""")
    lista_medidas = cur.fetchall()
    largura = 0
    altura = 0
    for medida in lista_medidas:
        largura+=medida[3]
        altura+=medida[4]
    largura=largura/len(lista_medidas)
    altura=altura/len(lista_medidas)
    return largura, altura

def Dist_quad(cur, id_quad_sem, id_quad_com):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE Id = ?""", (id_quad_sem,))
    quad_sem_med = cur.fetchall()[0]
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE Id = ?""", (id_quad_com,))
    quad_com_med = cur.fetchall()[0]
    dist_x = (quad_sem_med[1] - quad_com_med[1])*(quad_sem_med[1] - quad_com_med[1])
    dist_y = (quad_sem_med[2] - quad_com_med[2])*(quad_sem_med[2] - quad_com_med[2])
    return (dist_x + dist_y)

def Salvar_MedidaFinal(cur):
    cur.execute("""SELECT * FROM 'Quadrantes'""")
    lista_quadrantes = cur.fetchall()
    quadrantes_sem_medidas = []
    #para quadrantes que tem medidas
    quadrantes_com_medidas = []
    for quadrante in lista_quadrantes:
        Quadranteid = quadrante[0]
        cur.execute("""SELECT * FROM 'MedidaParcial' WHERE Quadranteid = ?""", (Quadranteid,))
        lista_medidas = cur.fetchall()
        if (len(lista_medidas)==0):
            quadrantes_sem_medidas.append(Quadranteid)
        else:
            quadrantes_com_medidas.append(Quadranteid)
            largura, altura = Media_Medidas(lista_medidas)
            valores_input = (None, largura, altura, Quadranteid)
            cur.execute("""INSERT INTO MedidaFinal VALUES (?,?,?,?)""", valores_input)
    #para quadrantes que nao tem
    

    ## achar quadrante mais proximo 
    for id_quad_sem in quadrantes_sem_medidas:
        distancia_menor = []
        quadrante_mais_perto = []
        for id_quad_com in quadrantes_com_medidas:
            #print (id_quad_com)
            distancia = Dist_quad(cur, id_quad_sem, id_quad_com)
            if (len(distancia_menor) == 0):
                distancia_menor.append(distancia)
                quadrante_mais_perto.append(id_quad_com)
            elif (distancia_menor[0]>distancia):
                distancia_menor[0] = distancia
                quadrante_mais_perto[0] = id_quad_com
        #testa na altura dele
        cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid = ?""", (quadrante_mais_perto[0],))
        obj_medida_final = cur.fetchall()[0]
        largura = obj_medida_final[1]
        altura = obj_medida_final[2]
        valores_input = (None, largura, altura, id_quad_sem)
        cur.execute("""INSERT INTO MedidaFinal VALUES (?,?,?,?)""", valores_input)
    return





#cur.execute("CREATE TABLE MedidaFinal(Id INTEGER PRIMARY KEY AUTOINCREMENT, Width INT, Height INT, Quadrante INT, FOREIGN KEY(Quadrante) REFERENCES Quadrante(Id))")