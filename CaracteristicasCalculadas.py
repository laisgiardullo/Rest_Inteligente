import numpy as np
import cv2
#from autocanny import *
from METHODS import *
import Person
import time
import sqlite3 as lite
import sys
import datetime

from variaveis_globais import * #w_frame etc aqui
from MatrizPixels import *
from Deteccao import *
from ApoioDeteccao import *
from Posicionamento import *

def Largura_Media(x, y, cur):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (x, x, y, y,))
    quadrante = cur.fetchall()
    quadrante_id = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadrante_id=?""", (quadrante_id,))
    medida = (cur.fetchall())[0]
    largura_media = medida[1]
    return (largura_media)

def Salvar_DataHora(now, cur):
    ano = now.year
    mes = now.month
    dia = now.day
    hora = now.hour
    minuto = now.minute
    segundo = now.second
    milissegundo = now.microsecond
    objeto = (None, dia, mes, ano, hora, minuto, segundo, milissegundo)
    cur.execute("INSERT INTO DataHora VALUES(?,?,?,?,?,?,?,?)", objeto)
    cur.execute("""SELECT * FROM 'DataHora' ORDER BY Id""")
    lista_dh = cur.fetchall()
    id_now = lista_dh[len(lista_dh)-1][0]
    return (id_now)

def SalvarNumPessoasTotal(now_id, cur):
    cur.execute("""SELECT * FROM 'Pessoa' Where Status='in'""")
    lista_pessoas = cur.fetchall()
    num_pessoas = len(lista_pessoas)
    objeto = (None, num_pessoas, now_id)
    cur.execute("INSERT INTO NumeroPessoasTotal VALUES(?,?,?)", objeto)
    return
