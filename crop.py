# import the necessary packages
import argparse
import cv2
import numpy as np
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False


def crop_objetos (event,x,y,flags,param):

        #Nessa funcao o usuario seleciona uma regiao que o usuario quer observar, atraves de 4 pontos que ele escolhe para selecionar a imagem.
        #Aparecem linhas ao redor das regioes de interesse. Se ele quiser resertar o recorte, aperta a tecla r
        
    lista_objetos = dist = []
    points=4
    pontos = pid = i = 0
    linha = points
    #cur = con.cursor()
    #image = cv2.imread(frame)
    #cv2.namedWindow(image)
    cv2.setMouseCallback('image', crop_objetos)
    key = cv2.waitKey(1) & 0xFF

    while pontos<points:

        if key == ord("r"):
            pontos = 0
        #captura os pontos clicados na imagem
        elif event == cv2.EVENT_LBUTTONDOWN:
            print(x)
            print(y)
            lista_objetos.append([x,y])
            pontos += 1
#desenhar as linhas para os pontos selecionados
    while linha>0:
            cv2.line(img, lista_objetos[i], lista_objetos[i+1], color, thickness=1, lineType=8, shift=0)
            linha -= 1    
            dist.append(math.hypot(lista_objetos[i+1][i] - lista_objetos[i][i], lista_objetos[i+1][i+1] - lista_objetos[i][i+1]))

    return(points)


def crop_pessoas(event, x, y, flags, param):

        #a funcao recortar uma pessoa na imagem e retorna os valores desejados dessa pessoa

        
        # grab references to the global variables
        global refPt, cropping
 
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
                refPt = [(x, y)]
                cropping = True
 
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
                # record the ending (x, y) coordinates and indicate that
                # the cropping operation is finished
                refPt.append((x, y))
                cropping = False
 
                # draw a rectangle around the region of interest
                cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
                #for i in range(len(refPt)-1):
                #    a = refPt[i][0]
                ##    b = refPt[i][1]
                #    c = refPt[i+1][0]
                #    d = refPt[i+1][1]
                #    image = cv2.line(image, (a,b),(c,d), (0,255,0), 2)
                #cv2.imshow("image", image)

# construct the argument parser and parse the arguments
image = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)



#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
#image = cv2.imread(args["image"])
#clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", crop_objetos)
 
# keep looping until the 'q' key is pressed
while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
 
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
                image = clone.copy()
 
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
                break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        largura = refPt[1][0] - refPt[0][0]
        altura = refPt[1][1] - refPt[0][1]
        xmedium = largura/2
        ymedium = altura/2
        # (refPt[0][0])
        #print (refPt[0][1])
        #print (refPt[1][0])
        #print(refPt[1][1])
        print ("A largura da imagem e de", largura)
        print ("A altura da imagem e de", altura)        
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)
        #return(xmedium,ymedium,largura,altura)
 
# close all open windows
cv2.destroyAllWindows()



def recortar_pessoas (frame):

    #Essa funcao pega as informacoes das pessoas obtidas em crop_pessoas e joga esses valores no banco de dados
    #
    lista_medidas = []
    pid = 0
    cur = con.cursor()
    image = cv2.imread(frame)
    cv2.namedWindow(image)
    cv2.setMouseCallback(image, recortar_pessoas)

    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
 
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
                image = clone.copy()
 

        # if the 'Esc' key is pressed, break from the loop
        elif key == ord("27"):
                break

        else:
                lista_medidas=crop()
                pid+= 1
                #mandar dados para banco de dados
                cur.execute("INSERT INTO Medidas VALUES(?,?,?,?,?)",[pid]+lista_medidas)
                lista_medidas=[]
                return (pid)

    # close all open windows
    cv2.destroyAllWindows()


	




#def recortar objetos:

          #Nessa funcao o usuario seleciona todas as regioes do video em que ele quer observar (chama funcao crop)

        






