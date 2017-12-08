#documento com funcoes utilizadas pelos metodos de deteccao

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
from ApoioDeteccao import *
from CaracteristicasCalculadas import *
from Posicionamento import *



def Media_Pessoas_Frames(quantidade_frames_considerados, num_frame, persons):
    num_frame_maximo = num_frame - quantidade_frames_considerados # faco a media com os ultimos 8 frames
    num_pessoas_media = 0
    qnr_frames_inicio = 0
    if (num_frame_maximo<0): #se ainda nao passou da qnt de frames considerados (inicio do video), media de todos os anteriores
        for i in persons:
            num_pessoas_media+=1
        if (num_frame > 0):
            num_pessoas_media = num_pessoas_media/num_frame
    else:
        for i in persons:
            if (i.frame > num_frame_maximo):
                num_pessoas_media+=1
        num_pessoas_media = num_pessoas_media/quantidade_frames_considerados
    return (num_pessoas_media)

def Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, novos_pts, con):
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
            #persons.append(p)
            pid += 1
            #########   EXPLICACAO LOGICA   ###########
            ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
            img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
            it+=new_width
            pa = np.array ([[cx]])
            pb = np.array ([[cy]])
            nv_pt = np.dstack((pa,pb))
            nv_pt = nv_pt.astype(np.float32)
            if (num_frame>20): #so comeca a guardar depois do 21 que eh quando estabiliza o background
                if (novos_pts !=[]):
                    novos_pts = np.append(novos_pts,nv_pt, axis = 0)
                else: novos_pts = nv_pt
    if (lista_obj!=[]):
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
            cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
    return (pid, novos_pts)

def Tranformar_em_Numpy(lista_posicoes):
    pontos_numpy = []
    for elemento in lista_posicoes:
        pa = np.array ([[elemento[1]]]) #X eh salvo na posicao 6 do objeto posicao
        pb = np.array ([[elemento[2]]]) #Y eh salvo na posicao 6 do objeto posicao
        nv_pt = np.dstack((pa,pb))
        nv_pt = nv_pt.astype(np.float32)
        if (pontos_numpy !=[]):
            pontos_numpy = np.append(pontos_numpy,nv_pt, axis = 0)
        else: pontos_numpy = nv_pt
    return(pontos_numpy)

def Atualizar_Posicoes(objetos_ativos, novos_pts, novos_pts_prox, tempo_video, cur, mask, frame, contours1):
    mask_novo = mask
    for ponto in range (len(novos_pts)):
        
        antigo_x = int(novos_pts[ponto][0][0])
        novo_x = int(novos_pts_prox[ponto][0][0])
        #print("novo_x="+str(novo_x))
        antigo_y = int(novos_pts[ponto][0][1])
        novo_y = int(novos_pts_prox[ponto][0][1])

        id_posicao = objetos_ativos[ponto][0]
        id_pessoa = objetos_ativos[ponto][6]
        #se valores forem diferentes
        mudou = False
        if ((antigo_x!=novo_x) or (antigo_y!=novo_y)):
            for cnt in contours1:
                dentro_contorno = cv2.pointPolygonTest(cnt, (novo_x, novo_y), False) 
                if (dentro_contorno>0 and mudou==False):
                    cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Id = ?""", (tempo_video, id_posicao))
                    #sakila.execute("SELECT first_name, last_name FROM customer WHERE last_name = ?",(last,))
                    valores_input = (None, int(novo_x), int(novo_y), tempo_video, None, 1, id_pessoa)
                    cur.execute("""INSERT INTO Posicao VALUES (?,?,?,?,?,?,?)""", valores_input)
                    mudou = True
                    mask_novo = cv2.line(mask_novo, (antigo_x,antigo_y),(novo_x,novo_y), (0,255,0), 2)
                    mask_novo = cv2.circle(mask_novo,(novo_x,novo_y),5,(0,255,0),-1)
        mask_novo = cv2.putText(mask_novo, str(id_pessoa), (novo_x, novo_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
    img = cv2.add(frame,mask_novo)
    cv2.imshow('frame_optflow',img)

    return

def Atualizar_Status(tempo_video, cur):
    cur.execute("""SELECT * FROM 'Posicao' WHERE (X>?-? OR X<? OR Y>?-? OR Y<?) AND Atual=1""", (w_frame, largura_padrao, largura_padrao, h_frame, altura_padrao, altura_padrao))
    lista_fora = cur.fetchall()
    for obj in lista_fora:
        id_posicao_atualizar = obj[0]
        id_pessoa_atualizar = obj[6]
        cur.execute("""UPDATE Pessoa SET Instante_Saida = ?, Status = "out" WHERE Id=?""", (tempo_video, id_pessoa_atualizar))
        cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Id=?""", (tempo_video, id_posicao_atualizar))
    return

def Imprimir_Novo_Objeto(texto, pid, cx, cy, num_contorno):
    ## XX EXCLUIR APOS TESTES XX ##
    print ("NOVO OBJETO")
    print ("ID:"+str(pid))
    print ("Cx:"+str(cx)+" Cy:"+str(cy))
    print ("Num Contorno:"+str(num_contorno))
    ## XX EXCLUIR APOS TESTES XX ##

    texto.append('\n \n NOVO OBJETO: ID '+str(pid))
    texto.append("\n Cx:"+str(cx)+" Cy:"+str(cy))
    texto.append("\n Num Contorno:"+str(num_contorno))
    texto.append('\n \n ')
    return(texto)

def Imprimir_ObjetoseTracks(texto, pessoas2, i):
    print (" ")
    print ("Pessoas:")
    print (pessoas2)
    print ("id:"+str(i.i))
    print(i.x)
    print(i.y)
    print (i.tracks)
    print (i.status)

    texto.append("\n Pessoas:"+str(pessoas2))
    texto.append('\n ID '+str(i.i))
    texto.append("\n (CX,CY) = ("+str(i.x)+","+str(i.y)+")")
    texto.append('\n Tracks: '+str(i.tracks))
    texto.append('\n Status '+str(i.status))
    texto.append(' \n \n')
    return(texto)



def Salvar_Mostrar_PessoaMet1(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, con):
    print("entrei no metodo")
    it = 0 #it = iteracao
    lista_obj = []
    lista_obj_pos = []
    cur = con.cursor()
    mask_novo = img
    for i in range (pp):
        novo = True
        new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)
        novo, id_pessoa, id_posicao = Pessoa_Nova(cx, new_width, cy, cur, tempo_video)
        print (novo)
        if (novo and cx>largura_padrao and cx<(w_frame-largura_padrao) and cy>altura_padrao and cy<(h_frame-altura_padrao)):
            print ("sounovo")
            #p = Person.Pessoa_Pontual(pid,cx,cy, new_width, num_frame,tempo_video)
            #(Id INT, X INT, Y INT, Status TEXT, Width INT, Num_Frame INT, Instante INT)")
            #obj_pessoa = (Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)

            lista_obj.append((pid,'in',new_width,tempo_video, None))
            lista_obj_pos.append((None, cx, cy, tempo_video, None, 1, pid))
            #persons.append(p)
            pid += 1
            #########   EXPLICACAO LOGICA   ###########
            ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
            img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
            it+=new_width

        else:
            print("sou velho")
            cur.execute("""UPDATE Posicao SET Instante_Final = ?, Atual = 0 WHERE Id = ?""", (tempo_video, id_posicao))
            #sakila.execute("SELECT first_name, last_name FROM customer WHERE last_name = ?",(last,))
            valores_input = (None, int(cx), int(cy), tempo_video, None, 1, id_pessoa)
            cur.execute("""INSERT INTO Posicao VALUES (?,?,?,?,?,?,?)""", valores_input)

            #mask_novo = cv2.line(mask_novo, (antigo_x,antigo_y),(novo_x,novo_y), (0,255,0), 2)
            mask_novo = cv2.circle(img,(cx,cy),5,(0,255,0),-1)
        mask_novo = cv2.putText(mask_novo, str(id_pessoa), (cx, cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
    cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
    cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
    img = cv2.add(img,mask_novo)
    cv2.imshow('frame_optflow',img)

    return (pid)

def Salvar_Mostrar_PessoaCnt(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, novos_pts, con, cnt):
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

            #persons.append(p)
            pid += 1
            #########   EXPLICACAO LOGICA   ###########
            ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
            img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
            it+=new_width
            pa = np.array ([[cx]])
            pb = np.array ([[cy]])
            nv_pt = np.dstack((pa,pb))
            nv_pt = nv_pt.astype(np.float32)
            if (num_frame>20): #so comeca a guardar depois do 21 que eh quando estabiliza o background
                if (novos_pts !=[]):
                    novos_pts = np.append(novos_pts,nv_pt, axis = 0)
                else: novos_pts = nv_pt
    if (lista_obj!=[]):
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
            cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
    return (pid, novos_pts)