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
from Posicionamento import *
from desenhar import *

#cap = cv2.VideoCapture('videos\Eletrica_Ent.mov') #Open video file
#cap = cv2.VideoCapture(r'videos\armarios_biblio.mov') #Open video file
#cap = cv2.VideoCapture('videos\Fila_Camera1.mp4') #Open video file
#cap = cv2.VideoCapture('videos\TownCentreXVID.avi') #Open video file
#cap = cv2.VideoCapture('videos\VISOR1.avi') #Open video file
#cap = cv2.VideoCapture('videos\Rest_Israel.mp4') #Open video file
#cap = cv2.VideoCapture('videos\Chinese_Rest.mp4') #Open video file
#cap = cv2.VideoCapture('videos\IMG_2409.mov')
#cap = cv2.VideoCapture('videos\Rest_Israel.mp4') #Open video file
cap = cv2.VideoCapture('videos\Refeitorio_Camera1.mp4') #Open video file
#cap = cv2.VideoCapture('videos\Estavel.mp4') #Open video file
#cap.set(3,160) #set width (3) para 160
#cap.set(4,90) #set height (4) para 90


persons = []
pid = 1
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=255, detectShadows=True) #Create the background substractor
nframe = 0
old_frame = 0
p0=[]
p1=[]
novos_pts = []


con = lite.connect(r'GUI\video_inteligente_gui\db.sqlite3')
cur = con.cursor()


frame_estabilizado = input("Digite o frame inicial para contagem")
limpar_tabela = input("Digite 1 para deletar todos registros existentes ou 0 para manter")

if(limpar_tabela==1):
    cur.execute("""DELETE FROM DataHora""")
    cur.execute("""DELETE FROM Quadrantes""")
    cur.execute("""DELETE FROM Pessoa""")
    cur.execute("""DELETE FROM Posicao""")
    cur.execute("""DELETE FROM PontoAtualInterno""")
    cur.execute("""DELETE FROM MedidaParcial""")
    cur.execute("""DELETE FROM MedidaFinal""")
    cur.execute("""DELETE FROM NumeroPessoasQuadrante""")
    cur.execute("""DELETE FROM Local""")
    cur.execute("""DELETE FROM NumeroPessoasLocal""")
    cur.execute("""DELETE FROM NumeroPessoasTotal""")

#areaTH = input("Area Minima Pessoa")
#tipo = input("Digite:\n 1 para seguir (metodo 1) \n 2 para optical flow\n 3 para cascade \n 4 para metodo 1 manual")
tipo = 5
salto_Opt_Flow = input("Digite de quantos em quantos quadros voce deseja fazer o optical flow")

Inicializar_Quadrantes(cur)

ret, frame = cap.read()
Sret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()
ret, frame = cap.read()

frame = cv2.resize(frame, (w_frame, h_frame))
calibracao = input("digite 1 para calibracao ou 0 para continuar")

if(calibracao==1):
    DesenharPessoas(frame, cur)
    DesenharAreasDeteccao(frame, cur)
    DesenharAreasDescarte(frame, cur)
    Salvar_MedidaFinal(cur)

largurafinal_geral,alturafinal_geral  = TotalMedidaFinal(cur)

areaTH = (largurafinal_geral*alturafinal_geral)/2

if (tipo == 1):
    while(cap.isOpened()):
        ret, frame = cap.read() #read a frame
        frame = cv2.resize(frame, (w_frame, h_frame))
        tempo_video = cap.get(0)
        #frame2 = Cascade1(frame)
        #frame2 = Countours (frame, fgbg)
        contours1 = Countours_Area_Pontual(frame, fgbg, persons, pid, nframe, tempo_video, novos_pts, con)
        if(nframe>frame_estabilizado):
            #Utilizando metodo de seguir pessoas:
            frame2 , pid, novos_pts = Determinar_Pessoa(contours1, frame, areaTH, pid, nframe, tempo_video, novos_pts, con, 1)
        #frame2, persons, pid = Countours_Area(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video, con, 1)
            Atualizar_Status(tempo_video, cur)
            cv2.imshow('Frame',frame2)
        nframe +=1
        #Abort and exit with 'Q' or ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            con.commit()
            con.close()
            break
elif (tipo ==2):
    ret, old_frame = cap.read() #read a frame
    old_frame = cv2.resize(old_frame, (w_frame, h_frame))
    a=np.array([]) #todos x na ordem
    b=np.array([]) #todos y na ordem
    novos_pts = []
    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    #novos_pts = np.dstack((a,b))
    #novos_pts = novos_pts.astype(np.float32) #mudar tipo de objetos do array para float32
    while(cap.isOpened()):
        ret, frame = cap.read() #read a frame
        frame = cv2.resize(frame, (w_frame, h_frame))
        tempo_video = cap.get(0)
        contours1 = Countours_Area_Pontual(frame, fgbg, persons, pid, nframe, tempo_video, novos_pts, con)
        if(nframe>frame_estabilizado):
            frame2 , pid, novos_pts = Determinar_Pessoa(contours1, frame, areaTH, pid, nframe, tempo_video, novos_pts, con, 2)


        #frame2, persons, pid = Countours_Area(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
        #frame2, persons, pid = Countours_Area_Door(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
        #frame2, persons, pid, old_frame,p0 = Countours_Area_Seguir(frame, fgbg, persons, pid, max_p_age,nframe, tempo_video, old_frame,p0, p1)
        #if(novos_pts!=[]):
        #    novos_pts = novos_pts.reshape(-1,1,2)
        #p0 = np.dstack((lista_cx,lista_cy))
        #p0 = p0.astype(np.float32)
        cur.execute("""SELECT * FROM 'Posicao' WHERE Atual=1""")
        objetos_ativos = cur.fetchall() #resultado inteiro da ultima selecao
        novos_pts = Tranformar_em_Numpy(objetos_ativos)
        print("novos_pts="+str(novos_pts))
        if (novos_pts!=[] and nframe>frame_estabilizado and nframe%15==0):
            novos_pts_prox, mask = OptFlow(old_frame, frame, novos_pts, mask) #tem que transformar esses novos pts em p0...
            Atualizar_Posicoes(objetos_ativos, novos_pts, novos_pts_prox, tempo_video, cur, frame2, mask, contours1)
            old_frame = frame
        Atualizar_Status(tempo_video, cur)
            #novos_pts = novos_pts_prox
        #cv2.imshow('Frame',frame2)
        nframe +=1
        
        
        #Abort and exit with 'Q' or ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            con.commit()
            con.close()
            break
elif (tipo ==3):
     while(cap.isOpened()):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (w_frame, h_frame))
        frame2 = Cascade(frame)
        cv2.imshow('Frame',frame2)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
elif (tipo == 4):
    while(cap.isOpened()):
        ret, frame = cap.read() #read a frame
        tempo_video = cap.get(0)
        #frame2 = Cascade1(frame)
        #frame2 = Countours (frame, fgbg)
        frame2, persons, pid = Countours_Area_Door(frame, fgbg, persons, pid, nframe, tempo_video)
        cv2.imshow('Frame',frame2)
        nframe +=1
        #Abort and exit with 'Q' or ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
elif (tipo ==5):
    matriz_flow = None
    ret, old_frame = cap.read() #read a frame
    old_frame = cv2.resize(old_frame, (w_frame, h_frame))
    mask = np.zeros_like(old_frame)
    lista = []
    while(cap.isOpened()):
        now = datetime.datetime.now()
        now_id = Salvar_DataHora(now, cur)

        ret, frame = cap.read() #read a frame
        frame = cv2.resize(frame, (w_frame, h_frame))
        tempo_video = cap.get(0)
        contours1 = Countours_Area_Pontual(frame, fgbg, persons, pid, nframe, tempo_video, novos_pts, con)
        if(nframe>frame_estabilizado):
            frame2 , pid = Comparar_e_Salvar_Novos2(contours1, frame, areaTH, pid, nframe, tempo_video, con)
            if (nframe%salto_Opt_Flow==0):
                matriz_flow = OptFlowDense(old_frame, frame, matriz_flow)
                old_frame = frame
                Atualizar_PontosAtuaisInternos(matriz_flow, cur, frame, tempo_video)
                Limpar_PontosPerdidos2(cur, matriz_flow)
                #Atualizar_PontosAtuaisInternos2(matriz_flow, cur, frame)
                Atualizar_PosicoesFlow(cur, tempo_video, frame)

                SalvarNumPessoasTotal(now_id, cur)



        #frame2, persons, pid = Countours_Area(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
        #frame2, persons, pid = Countours_Area_Door(frame, fgbg, persons, pid, max_p_age, nframe, tempo_video)
        #frame2, persons, pid, old_frame,p0 = Countours_Area_Seguir(frame, fgbg, persons, pid, max_p_age,nframe, tempo_video, old_frame,p0, p1)
        #if(novos_pts!=[]):
        #    novos_pts = novos_pts.reshape(-1,1,2)
        #p0 = np.dstack((lista_cx,lista_cy))
        #p0 = p0.astype(np.float32)
        #cur.execute("""SELECT * FROM 'Posicao' WHERE Atual=1""")
        #objetos_ativos = cur.fetchall() #resultado inteiro da ultima selecao
        #novos_pts = Tranformar_em_Numpy(objetos_ativos)
        #print("novos_pts="+str(novos_pts))
        #if (novos_pts!=[] and nframe>frame_estabilizado and nframe%15==0):
        #    novos_pts_prox, mask = OptFlow(old_frame, frame, novos_pts, mask) #tem que transformar esses novos pts em p0...
        #    Atualizar_Posicoes(objetos_ativos, novos_pts, novos_pts_prox, tempo_video, cur, frame2, mask, contours1)
        #    old_frame = frame
        #Atualizar_Status(tempo_video, cur)
            #novos_pts = novos_pts_prox
            cv2.imshow('Frame',frame2)
        nframe +=1
        
        
        #Abort and exit with 'Q' or ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            con.commit()
            con.close()
            break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows