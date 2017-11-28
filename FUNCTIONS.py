#documento com funcoes utilizadas pelos metodos de deteccao

import numpy as np
import cv2
#from autocanny import *
import Person
import time
import sqlite3 as lite
from variaveis_globais import *

def Inicializar_Quadrantes(cur):
    largura_quad = w_frame/raiz_n_quad
    altura_quad = h_frame/raiz_n_quad
    for i in range (raiz_n_quad):
        for j in range(raiz_n_quad):
            valores_input = (None, i, j,largura_quad*i, altura_quad*j, largura_quad, altura_quad, largura_padrao, altura_padrao)
            cur.execute("""INSERT INTO Quadrantes VALUES (?,?,?,?,?,?,?,?,?)""", valores_input)


#def Salvar_Largura_Altura_Quadrantes(cur):




def Pessoa_Nova(cx, new_width, cy, cur, tempo_video):
    xa = 31
    ya = 60
    limite = xa*xa+ya*ya
    cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X)+(?-Y)*(?-Y))<? AND Atual=1 AND Instante_Inicial!=? ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y))""", (cx, cx, cy, cy, limite, tempo_video, cx, cx, cy, cy, ))
    
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

def Largura_Media(x, y):
    largura_media = 31
    return (largura_media)

def Qnt_Pessoas_Contorno (w, largura_media):
    pp = w//largura_media
    if (pp==0):
        pp=1
    return (pp)

def Atualizar_Retangulo(x, y, h, new_width, it):
    new_x = x+it #novo valor de x, caso seja mais de 1 pessoa 
    cx = new_x + (new_width/2) #cx = o centro do retangulo da pessoa, em x
    cy = y + (h/2) #cy = o centro do retangulo da pessoa, em y
    return (new_x, cx, cy)

def Aplicacao_Mascara(fgmask):
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    #########   EXPLICACAO LOGICA    ###########
    #Vamos aplicar a mascara 
    #########   EXPLICACAO FUNCAO   ###########
    #threshold: If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
    #Adaptive thresholding: In this, the algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.
    #########   LINK   ###########
    #ver http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    imBin = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY_INV,11,2)

    ### XX OUTROS TESTES XX ###
    #ret,imBin = cv2.threshold(fgmask,127,255,cv2.THRESH_BINARY)
    #imBin2 = cv2.adaptiveThreshold(teste2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #    cv2.THRESH_BINARY_INV,11,2)
    #Opening (erode->dilate) para tirar ruido.
    ### XX OUTROS TESTES XX ###

    mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)

    ### XX OUTROS TESTES XX ###
    #mask2 = cv2.morphologyEx(teste2, cv2.MORPH_OPEN, kernelOp)
    #Closing (dilate -> erode) para juntar regioes brancas.
    #mask2 =  cv2.morphologyEx(mask2 , cv2.MORPH_CLOSE, kernelCl)
    ### XX OUTROS TESTES XX ###

    mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    return (mask)

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
        print("novo_x="+str(novo_x))
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