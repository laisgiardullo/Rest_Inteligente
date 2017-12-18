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
from CaracteristicasCalculadas import *
from desenhar import *


def Medidas_Media(x, y, cur):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (x, x, y, y,))
    quadrante = cur.fetchall()
    Quadranteid = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid=?""", (Quadranteid,))
    medida = (cur.fetchall())[0]
    largura_media = medida[1]
    altura_media = medida[2]
    return (largura_media, altura_media)


def Todas_Pessoas_Sairem(cur, tempo_video):
	cur.execute("""UPDATE Pessoa SET Instante_Saida = ?, Status = "out" """, (tempo_video,))
	cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Atual=1""", (tempo_video,))	
	cur.execute("""DELETE FROM 'PontoAtualInterno'""")

def PessoaSair(cur, id_pessoa, tempo_video):
    cur.execute("""UPDATE Pessoa SET Instante_Saida = ?, Status = "out" WHERE Id=?""", (tempo_video, id_pessoa,))
    cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Pessoa_id=? AND Atual=1""", (tempo_video, id_pessoa,))
    cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Pessoa_id=?""",(id_pessoa,))


def OptFlowDense(old_frame, frame, flow):
	mask = np.zeros_like(frame)
	next = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	prvs = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
	flow = cv2.calcOpticalFlowFarneback(prvs,next, flow, 0.5, 3, 15, 3, 5, 1.2, 0)
	return(flow)

def Atualizar_PontosAtuaisInternos(matriz_flow, cur, img, tempo_video):
	cur.execute("""SELECT * FROM 'PontoAtualInterno'""")
	lista_pontos = cur.fetchall()
	mask = np.zeros_like(img)
	for ponto in lista_pontos:
		x_ant = ponto[2] #x fica na posicao 2 do objeto
		y_ant = ponto[3]
		pessoa_id = ponto[4]
		ultima_mov = ponto[5]

		deslocamento_x = matriz_flow[int(y_ant)][int(x_ant)][0]
		deslocamento_y = matriz_flow[int(y_ant)][int(x_ant)][1]
		if (ultima_mov>0):
			deslocamento_total = int((abs(deslocamento_x) + abs(deslocamento_y))) + ultima_mov
		else:
			deslocamento_total = int((abs(deslocamento_x) + abs(deslocamento_y)))

		x_prox = x_ant + deslocamento_x
		y_prox = y_ant + deslocamento_y
		if (x_prox<=1 or x_prox>=w_frame-1 or y_prox <=1 or y_prox >(h_frame-1)):
			#PessoaSair(cur, pessoa_id, tempo_video)
			cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Id = ?""", (ponto[0],))

		else:
			cur.execute("""UPDATE PontoAtualInterno SET X = ?, Y = ?, Ultima_mov = ? WHERE Id = ?""", (x_prox, y_prox, deslocamento_total, ponto[0]))
	
		mask = cv2.line(mask, (int(x_ant),int(y_ant)),(int(x_prox),int(y_prox)), (0,255,0), 2)
		#mask = cv2.putText(mask, "AQUI", (int(x_prox),int(y_prox)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
		mask = cv2.circle(mask,(int(x_prox),int(y_prox)),5,(0,255,0),-1)
	frame2 = cv2.add(img,mask)
	cv2.imshow('flow',frame2)
	return


def Atualizar_PosicoesFlow(cur, tempo_video, img):
	mask = np.zeros_like(img)
	cur.execute("""SELECT * FROM 'Pessoa' WHERE Status='in'""")
	lista_pessoa = cur.fetchall()
	for pessoa in lista_pessoa:
		pessoa_id = int(pessoa[0])
		cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE Pessoa_id=?""", (pessoa_id,))
		lista_pontos = cur.fetchall()
		#print("listapts"+str(lista_pontos))
		numero_pts = len(lista_pontos)
		if (len(lista_pontos)==0):
			PessoaSair(cur, pessoa_id, tempo_video)
			#pass
		else:
			x_massa = 0
			y_massa = 0
			for ponto in lista_pontos:
				x_massa+=ponto[2]
				y_massa+=ponto[3]
			cx_novo = x_massa/numero_pts
			cy_novo = y_massa/numero_pts
			if (cx_novo<=1 or cx_novo>=w_frame-1 or cy_novo<=1 or cy_novo>(h_frame-1)):
				#PessoaSair(cur, pessoa_id, tempo_video)
				cur.execute("""DELETE * FROM 'PontoAtualInterno' WHERE Id = ?""", (ponto[0],))
				
			else:
				mask = cv2.circle(mask,(int(cx_novo),int(cy_novo)),5,(255,255,0),-1)
				if (imprimir_id == True):
					mask = cv2.putText(mask, str(pessoa_id), (int(cx_novo),int(cy_novo)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))

				cur.execute("""SELECT * FROM 'Posicao' WHERE Pessoa_id = ? and Atual = 1""", (pessoa_id,))
				pos_antiga = cur.fetchall()

				if (pos_antiga[0][1]!=int(cx_novo) or pos_antiga[0][2]!=int(cy_novo)):
					cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Id = ?""", (tempo_video, pos_antiga[0][0]))
					valores_input = (None, cx_novo, cy_novo, tempo_video, None, 1, pessoa_id)
					cur.execute("""INSERT INTO Posicao VALUES (?,?,?,?,?,?,?)""", valores_input)
	frame2 = cv2.add(img,mask)
	cv2.imshow('posicoes',frame2)
	return



def Limpar_PontosPerdidos_new(cur, matriz_flow):
	cur.execute("""SELECT * FROM 'Pessoa' WHERE Status ='in'""")
	lista_pes = cur.fetchall()
	for pes in lista_pes:
		pessoa_id = pes[0]
		print("pesid"+str(pessoa_id))
		cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE Pessoa_id=?""", (pessoa_id,))
		lista_ptos = cur.fetchall()
		lista_x = []
		lista_y = []
		if (len(lista_ptos)>0):
			for pto in lista_ptos:
				lista_x.append(pto[2])
				lista_y.append(pto[3])
			x_esquerda = min(lista_x)
			x_direita = max(lista_x)
			x_diferenca = x_direita - x_esquerda
			x_centro = x_esquerda + x_diferenca/2


			y_cima = min(lista_y)
			y_baixo = max(lista_y)
			y_diferenca = y_baixo - y_cima
			y_centro = y_cima + y_diferenca/2


			largura_media, altura_media = Medidas_Media(x_centro, y_centro, cur)

			qnt_largura = x_diferenca/largura_media
			qnt_altura = y_diferenca/altura_media

			if(qnt_largura>2 or qnt_altura>2):
				cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Pessoa_id=? AND Ultima_mov = 0""", (pessoa_id,))
			cur.execute("""UPDATE PontoAtualInterno SET Ultima_mov = ? WHERE Pessoa_id=?""", (None, pessoa_id))
	return


def Limpar_PtosAreasDescarte(cur, tempo_video):
	cur.execute("""SELECT * FROM 'Local' WHERE Tipo ='ignorar'""")
	locais_ign = cur.fetchall()
	for local in locais_ign:
		local_x = local[3]
		local_y = local[4]
		local_x_max = local_x + local[5]
		local_y_max = local_y + local[6]
		#cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X>=? AND X<=? AND Y>=? AND Y<=?""", (local_x, local_x_max, local_y, local_y_max,))
		cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE X>=? AND X<=? AND Y>=? AND Y<=?""", (local_x, local_x_max, local_y, local_y_max,))
		#lista_pontos_excluir = cur.fetchall()
		#for ponto in lista_pontos_excluir:
		#	id_pessoa = ponto[6]
		#	PessoaSair(cur, id_pessoa, tempo_video)
	return


