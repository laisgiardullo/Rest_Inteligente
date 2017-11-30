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
from Posicionamento import *

def Largura_Media(x, y):
    largura_media = 31
    return (largura_media)