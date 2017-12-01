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


def Salvar_MedidaFinal(cur):
    cur.execute("""SELECT * FROM 'Quadrantes'""")
    lista_quadrantes = cur.fetchall()
    quadrantes_sem_medidas = []
    #para quadrantes que tem medidas
    for quadrante in lista_quadrantes:
        quadrante_id = quadrante[0]
        cur.execute("""SELECT * FROM 'MedidaParcial' WHERE Quadrante_id = ?""", (quadrante_id,))
        lista_medidas = cur.fetchall()
        if (len(lista_medidas)==0):
            quadrantes_sem_medidas.append(quadrante_id)
        else:
            largura, altura = Media_Medidas(lista_medidas)
            valores_input = (None, largura, altura, quadrante_id)
            cur.execute("""INSERT INTO MedidaFinal VALUES (?,?,?,?)""", valores_input)
    #para quadrantes que nao tem
    for quad in quadrantes_sem_medidas:
        largura = 0
        altura = 0
        cur.execute("""SELECT * FROM 'Quadrantes' WHERE Id = ?""", (quad,))
        quadrante_atual = (cur.fetchall())[0]
        #Quadrantes(Id INTEGER PRIMARY KEY AUTOINCREMENT, N_Quad_X INT, N_Quad_Y INT, X INT, Y INT, Width INT, Height INT, W_Pessoa INT, H_Pessoa INT)")
        n_quad_y = quadrante_atual[4]
        h = quadrante_atual[6]
        
        #testa na altura dele
        cur.execute("""SELECT * FROM 'MedidaParcial' WHERE Y = ?""", (n_quad_y,))
        lista_medidas_ny = cur.fetchall()
        if (len(lista_medidas_ny)==0):
            nao_achou = True
        else:
            nao_achou = False
            largura, altura = Media_Medidas(lista_medidas_ny)
            valores_input = (None, largura, altura, quad)
            cur.execute("""INSERT INTO MedidaFinal VALUES (?,?,?,?)""", valores_input)
        if (nao_achou):
            cur.execute("""SELECT * FROM 'MedidaParcial'""")
            lista_medidas_t = cur.fetchall()
            if (len(lista_medidas_t)>0):
                largura, altura = Media_Medidas(lista_medidas_t)
            else:
                largura = largura_padrao
                altura = altura_padrao
            valores_input = (None, largura, altura, quad)
            cur.execute("""INSERT INTO MedidaFinal VALUES (?,?,?,?)""", valores_input)
        # i=0
        #ny_atual_baixo = n_quad_y + i
        # while (nao_achou and (ny_atual_baixo<h_frame or ny_atual_cima>=0)):
        #     ny_atual_baixo = n_quad_y + i


        #     i+=1
    return




#cur.execute("CREATE TABLE MedidaFinal(Id INTEGER PRIMARY KEY AUTOINCREMENT, Width INT, Height INT, Quadrante INT, FOREIGN KEY(Quadrante) REFERENCES Quadrante(Id))")