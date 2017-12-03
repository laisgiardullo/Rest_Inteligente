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






def PessoaSair(cur, id_pessoa, tempo_video):
    cur.execute("""UPDATE Pessoa SET Instante_Saida = ?, Status = "out" WHERE Id=?""", (tempo_video, id_pessoa,))
    cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Pessoa_id=? AND Atual=1""", (tempo_video, id_pessoa,))
    cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Pessoa_id=?""",(id_pessoa,))

def OptFlow(old_frame, frame, p0, mask):
			#fonte: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

	# Parameters for lucas kanade optical flow
	lk_params = dict( winSize  = (15,15),
					  maxLevel = 2,
					  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
	 
	# Create some random colors
	#color = np.random.randint(0,255,(100,3))
	old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# calculate optical flow
	p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
	print("p1: "+str(p1))

	 # Select good points
	#good_new = p1[st==1] #status==1: flow foi encontrado
	#good_old = p0[st==1]
	#print("good_new:"+str(good_new))
	#print("good_old:"+str(good_new))
	# # draw the tracks

	# #ZIP x = [1, 2, 3], y = [4, 5, 6], zip(x, y) =[(1, 4), (2, 5), (3, 6)]
	# #ENUMERATE seasons = ['Spring', 'Summer', 'Fall', 'Winter'], list(enumerate(seasons)) = [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
	# # i = numero do enumerate, new = elemento do good_new, old = elemento do good_old
	# for i,(new,old) in enumerate(zip(good_new,good_old)):
	for i,(new,old) in enumerate(zip(p1,p0)):
		a,b = new.ravel() #ravel: A 1-D array, containing the elements of the input, is returned
		c,d = old.ravel()
		#if((a,b)!=(c,d)):
		mask = cv2.line(mask, (a,b),(c,d), (0,255,0), 2)
		frame = cv2.circle(frame,(a,b),5,(0,255,0),-1)

	img = cv2.add(frame,mask)

	cv2.imshow('frame_22',img)

	# # Now update the previous frame and previous points
	old_gray = frame_gray.copy()
	# #p0 = good_new.reshape(-1,1,2)
	#if(len(good_new)==len(p1)):
	#    try:
	#        print("gnr:"+str(good_new.reshape(-1,1,2)))
	#        good_new = good_new.reshape(-1,1,2) #voltar ao formato original de p0
	#        novos_pts = good_new
	#    except:
	#        pass
	novos_pts = p1
	return (novos_pts, mask)
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

		deslocamento_x = matriz_flow[int(y_ant)][int(x_ant)][0]
		deslocamento_y = matriz_flow[int(y_ant)][int(x_ant)][1]

		x_prox = x_ant + deslocamento_x
		y_prox = y_ant + deslocamento_y
		if (x_prox<=1 or x_prox>=w_frame-1 or y_prox <=1 or y_prox >(h_frame-1)):
				PessoaSair(cur, pessoa_id, tempo_video)
				#cur.execute("""DELETE * FROM 'PontoAtualInterno' WHERE Id = ?""", (ponto[0],))

		cur.execute("""UPDATE PontoAtualInterno SET X = ?, Y = ? WHERE Id = ?""", (x_prox, y_prox, ponto[0]))
	
		mask = cv2.line(mask, (int(x_ant),int(y_ant)),(int(x_prox),int(y_prox)), (0,255,0), 2)
		#mask = cv2.putText(mask, "AQUI", (int(x_prox),int(y_prox)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
		mask = cv2.circle(mask,(int(x_prox),int(y_prox)),5,(0,255,0),-1)
	frame2 = cv2.add(img,mask)
	cv2.imshow('flow',frame2)
	return

def Atualizar_PontosAtuaisInternos2(matriz_flow, cur, img, tempo_video):
	cur.execute("""SELECT * FROM 'Pessoa' WHERE Status='in'""")
	lista_pessoa = cur.fetchall()
	for pessoa in lista_pessoa:
		pessoa_id = int(pessoa[0])
		cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE Pessoa_id=?""", (pessoa_id,))
		lista_pontos = cur.fetchall()
		mask = np.zeros_like(img)
		deslocamento_x_med = 0
		deslocamento_y_med = 0
		num_desl = len(lista_pontos)
		for ponto in lista_pontos:
			x_ant = ponto[2] #x fica na posicao 2 do objeto
			y_ant = ponto[3]

			deslocamento_x = matriz_flow[int(y_ant)][int(x_ant)][0]
			deslocamento_y = matriz_flow[int(y_ant)][int(x_ant)][1]

			deslocamento_x_med +=deslocamento_x
			deslocamento_y_med +=deslocamento_y

		deslocamento_x_med = deslocamento_x_med/num_desl
		deslocamento_y_med = deslocamento_y_med/num_desl
		for ponto in lista_pontos:
			x_ant = ponto[2] #x fica na posicao 2 do objeto
			y_ant = ponto[3]

			x_prox = x_ant + deslocamento_x_med
			y_prox = y_ant + deslocamento_y_med


			cur.execute("""UPDATE PontoAtualInterno SET X = ?, Y = ? WHERE Id = ?""", (x_prox, y_prox, ponto[0]))
		
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
		numero_pts = len(lista_pontos)
		if (len(lista_pontos)==0):
			PessoaSair(cur, pessoa_id, tempo_video)
		else:
			x_massa = 0
			y_massa = 0
			for ponto in lista_pontos:
				x_massa+=ponto[2]
				y_massa+=ponto[3]
			cx_novo = x_massa/numero_pts
			cy_novo = y_massa/numero_pts
			if (cx_novo<=1 or cx_novo>=w_frame-1 or cy_novo<=1 or cy_novo>(h_frame-1)):
				PessoaSair(cur, pessoa_id, tempo_video)
				#cur.execute("""DELETE * FROM 'PontoAtualInterno' WHERE Id = ?""", (ponto[0],))
			else:
				mask = cv2.circle(mask,(int(cx_novo),int(cy_novo)),5,(255,0,0),-1)

				cur.execute("""SELECT * FROM 'Posicao' WHERE Pessoa_id = ? and Atual = 1""", (pessoa_id,))
				pos_antiga = cur.fetchall()

				if (pos_antiga[0][1]!=int(cx_novo) or pos_antiga[0][2]!=int(cy_novo)):
					cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Id = ?""", (tempo_video, pos_antiga[0][0]))
					valores_input = (None, cx_novo, cy_novo, tempo_video, None, 1, pessoa_id)
					cur.execute("""INSERT INTO Posicao VALUES (?,?,?,?,?,?,?)""", valores_input)
	frame2 = cv2.add(img,mask)
	cv2.imshow('posicoes',frame2)
	return

def Limpar_PontosPerdidos(cur):
	cur.execute("""SELECT * FROM 'Posicao' WHERE Atual =1""")
	lista_pos = cur.fetchall()
	for pos in lista_pos:
		pessoa_id = pos[6]
		x_pos = pos[1]
		y_pos = pos[2]
		largura_media = Largura_Media(x_pos, y_pos, cur)
		altura_media = Altura_Media(x_pos, y_pos, cur)
		cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE Pessoa_id=?""", (pessoa_id,))
		lista_pontos = cur.fetchall()
		for ponto in lista_pontos:
			x_ponto=ponto[2]
			y_ponto=ponto[3]
			id_ponto = ponto[0]
			dist_quad_max = largura_media*largura_media + altura_media*altura_media
			dist_quad_x = (x_pos-x_ponto)*(x_pos-x_ponto)
			dist_quad_y = (y_pos-y_ponto)*(y_pos-y_ponto)
			if((dist_quad_y+dist_quad_x)>=dist_quad_max):
				cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Id=?""",(id_ponto,))
	return


