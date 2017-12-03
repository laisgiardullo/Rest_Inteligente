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

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
pontos_linhas = [[], []]


# mouse callback function
def draw_lines(event,x,y,flags,param):
    global ix,iy,drawing,mode
    #line2 = np.array([[200,500], [5,100]], np.int32).reshape((-1,1,2))
    #img = cv2.polylines(img,[line2],False,(0,0,255),thickness=1)


    if event == cv2.EVENT_LBUTTONDOWN:
        print("entrei clique")
        drawing = True
        ix,iy = x,y
        param[0].append((x,y))
        print(param[0])
    #enquanto mouse se move
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                param[0].append((x,y))
                #cv2.line(image, (ix,iy),(x,y), (0,255,0), 2)
                #cv2.rectangle(image,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(image,(x,y),5,(0,0,255),-1)
    if (len(param[0])==2):
        a = param[0][0]
        b = param[0][1]
        xa = a[0]
        ya = a[1]
        xb = b[0]
        yb = b[1]
        linha = np.array([[xa,ya], [xb,yb]], np.int32).reshape((-1,1,2))
        param[1].append(linha)
        param[0] = []

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.polylines(image, param[1], True, (0,255,0), 2)
            param[1] =[]
            #cv2.rectangle(image,(ix,iy),(x,y),(0,255,0),-1)
            #cv2.line(image, (ix,iy),(x,y), (0,255,0), 2)
        else:
            cv2.circle(image,(x,y),5,(0,0,255),-1)

    return param


def draw_rect(event,x,y,flags,param):
    global ix,iy,drawing,mode
    #primeiro ponto
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    #enquanto mouse se move
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(0,255,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(0,255,0),-1)
            SalvarMedidaParcial(ix, iy, x, y, param[1])

def draw_areasdeteccao(event,x,y,flags,param):
    global ix,iy,drawing,mode
    #primeiro ponto
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    #enquanto mouse se move
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(0,0,255),-1)
            SalvarAreaDeteccao(ix, iy, x, y, param[1])

def draw_areasdescarte(event,x,y,flags,param):
    global ix,iy,drawing,mode
    #primeiro ponto
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    #enquanto mouse se move
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(255,0,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(param[0],(ix,iy),(x,y),(255,0,0),-1)
            SalvarAreaDescarte(ix, iy, x, y, param[1])

def SalvarMedidaParcial(ix, iy, x, y, cur):
    x_meio = (ix+x)/2
    y_meio = (iy+y)/2
    Width_p = abs(x-ix)
    Height_p = abs(y-iy)
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (x_meio, x_meio, y_meio, y_meio,))
    quadrante = cur.fetchall()
    print(quadrante)
    quadrante_id = quadrante[0][0]
    print("qua"+str(quadrante_id))
    valores_input = (None, x_meio, y_meio, Width_p, Height_p, quadrante_id)
    cur.execute("""INSERT INTO MedidaParcial VALUES (?,?,?,?,?,?)""", valores_input)
    return

def SalvarAreaDeteccao(ix, iy, x, y, cur):
    nome = "detect"+str(ix)+","+str(iy)
    tipo = "fila"
    Width = abs(x-ix)
    Height = abs(y-iy)
    valores_input = (None, nome, tipo, ix, iy, Width, Height)
    cur.execute("""INSERT INTO Local VALUES (?,?,?,?,?,?,?)""", valores_input)
    return

def SalvarAreaDescarte(ix, iy, x, y, cur):
    nome = "descarte"+str(ix)+","+str(iy)
    tipo = "ignorar"
    Width = abs(x-ix)
    Height = abs(y-iy)
    valores_input = (None, nome, tipo, ix, iy, Width, Height)
    cur.execute("""INSERT INTO Local VALUES (?,?,?,?,?,?,?)""", valores_input)
    return







############MAIN

def DesenharPessoas(image, cur):
    #image = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('Desenhar Pessoas')
    #pontos_linhas = cv2.setMouseCallback('image',draw_lines,pontos_linhas)
    parametros = [image, cur]
    cv2.setMouseCallback('Desenhar Pessoas',draw_rect, parametros)

    while(1):
        cv2.imshow('Desenhar Pessoas',image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

    cv2.destroyAllWindows()

def DesenharAreasDeteccao(image, cur):
    #image = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('Areas Filas')
    #pontos_linhas = cv2.setMouseCallback('image',draw_lines,pontos_linhas)
    parametros = [image, cur]
    cv2.setMouseCallback('Areas Filas',draw_areasdeteccao, parametros)

    while(1):
        cv2.imshow('Areas Filas',image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

    cv2.destroyAllWindows()


def DesenharAreasDescarte(image, cur):
    #image = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('Areas Descarte')
    #pontos_linhas = cv2.setMouseCallback('image',draw_lines,pontos_linhas)
    parametros = [image, cur]
    cv2.setMouseCallback('Areas Descarte',draw_areasdescarte, parametros)

    while(1):
        cv2.imshow('Areas Descarte',image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

    cv2.destroyAllWindows()
