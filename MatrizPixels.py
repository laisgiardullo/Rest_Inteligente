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
