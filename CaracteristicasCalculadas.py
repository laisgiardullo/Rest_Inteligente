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
    Quadranteid = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid=?""", (Quadranteid,))
    medida = (cur.fetchall())[0]
    largura_media = medida[1]
    return (largura_media)

def Altura_Media(x, y, cur):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (x, x, y, y,))
    quadrante = cur.fetchall()
    Quadranteid = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid=?""", (Quadranteid,))
    medida = (cur.fetchall())[0]
    altura_media = medida[2]
    return (altura_media)

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

def SalvarNumPessoasLocal(now_id, cur):
    #cur.execute("CREATE TABLE Local(Id INTEGER PRIMARY KEY AUTOINCREMENT, Nome INT, Tipo TEXT, X INT, Y INT, Width INT, Height INT)") #tipo = tracking, fila ou ignorar
    objetos_num_locais = []
    cur.execute("""SELECT * FROM 'Local' Where Tipo!='ignorar'""")
    lista_locais = cur.fetchall()
    for local in lista_locais:
        local_id = local[0]
        local_x = local[3]
        local_x_max = local[3] + local[5]
        local_y = local[4]
        local_y_max = local[4] + local[6]
        cur.execute("""SELECT * FROM 'Posicao' Where Atual = 1 AND X>=? AND X<=? AND Y>=? AND Y<= ?""", (local_x, local_x_max, local_y, local_y_max,))
        pessoas = cur.fetchall()
        num_pessoas = len(pessoas)
        objetos_num_locais.append((None, num_pessoas, now_id, local_id))
    cur.executemany("INSERT INTO NumeroPessoasLocal VALUES(?,?,?,?)", objetos_num_locais)

    

