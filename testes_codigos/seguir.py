def Countours_Area_Seguir(img, fgbg, persons, pid, max_p_age, num_frame, tempo_video, old_frame2,p0, px):
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    color = np.random.randint(0,255,(100,3))
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'r')
    texto3 = arquivo3.readlines()
    arquivo3 = open('resultados/res_testes_excel_pontual.txt', 'w')

    #inicializacao de variaveis
    kernelOp = np.ones((3,3),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    areaTH = 100 # areaTH=area minima para considerar uma pessoa
    quantidade_frames_considerados = 8

    #Inicializacao de contadores
    num_pessoas = 0
    i=0
    n_cont=0
    if (num_frame==0):
        old_frame = img
        img2 = img
    #Aplicacao do substractor
    fgmask = fgbg.apply(img) #Use the substractor: aqui, o fundo, que nao esta mexendo, fica preto e o que esta se movimentando branco
    try:
        mask = Aplicacao_Mascara(fgmask)
    except:
        #se nao tem mais imagens para mostrar...
        print('EOF')

    #finding contours is like finding white object from black background. Object to be found should be white and background should be black.
    #cv2.RETR_EXTERNAL means we only care about external contours (contours within contours will not be detected) tentar RETR_TREE
    #cv2.CHAIN_APPROX_NONE is the algorithm used to make the contour
    #########   LINK   ###########
    #ver mais http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
    #ver hierarquia e contornos externos e internos em http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html

    

    __, contours1, hierarchy1 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    ### XX OUTROS TESTES XX ###
    #_, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours1)==0):
        maxlength = 1
        img2=img
        old_frame = img
    else: 
        #maxlength = max(map(len, contours1))
        #for cnt in contours1:
            ### XX OUTROS TESTES XX ###
                #contour = np.array(cnt,dtype = np.int32)
        #    for cnt2 in cnt:
                #contour_arr = np.zeros((maxlength, 1, 2), dtype=np.int32)
                #contour_arr[:len(cnt)] = cnt
        #        p0.append(cnt2)
        #p0 = np.array(p0).astype('object')
        #print (p0)
        #print ("fim")

    # Create a mask image for drawing purposes
        if(num_frame!=0):
            old_gray = cv2.cvtColor(old_frame2, cv2.COLOR_BGR2GRAY)
            mask2 = np.zeros_like(old_frame2)
            frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            num_contorno = 0
            lista_width = []
            if (num_frame==1):
                for cnt in contours1:
                    cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
                    area = cv2.contourArea(cnt)
                    
                    #########   LINK   ###########
                    #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
                    x,y,w,h = cv2.boundingRect(cnt) # x e y: top left
                    p0.append([x])
                    px.append([y])
                    print(p0)
                    largura_media = Largura_Media(x,y)
                    if (area>areaTH):
                        num_contorno+=1
                        pp = Qnt_Pessoas_Contorno(w, largura_media)
                        num_pessoas = num_pessoas + pp

                    ### XX OUTROS TESTES XX ###
                    #if (area>500 and w>40 and w<140 and h>70 and h<180):
                    ### XX OUTROS TESTES XX ###

                        new_width = w/pp #calcular a nova largura de somente 1 pessoa
                        lista_width.append(new_width)
                        persons, pid, novos_pts = Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, persons, num_frame,tempo_video)

                        ### XX OUTROS TESTES XX ###
                        #cv2.circle(img,(cx,cy), 5, (0,0,255), -1)           
                        #textw = "Width " + str(new_width)
                        #texth = "Height " + str(h)
                        ### XX OUTROS TESTES XX ###
                     # calculate optical flow
            
            #p0 = np.ndarray((len(p0,2)), buffer=np.array(p0), dtype=int)
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            print(p1)

            # Select good points
            good_new = p1[st==1]
            good_old = p0[st==1]

            # draw the tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                mask2 = cv2.line(mask2, (a,b),(c,d), color[i].tolist(), 2)
                img = cv2.circle(img,(a,b),5,color[i].tolist(),-1)
                img2 = cv2.add(img,mask)
            #########   EXPLICACAO LOGICA   ###########
            #Agora, vou percorrer todos os objetos de pessoas salvos e calcular o numero aproximado de pessoas baseado na media anterior
            num_pessoas_media = Media_Pessoas_Frames(quantidade_frames_considerados, num_frame, persons)
         
            texto3.append(str(num_pessoas)+";"+str(num_pessoas_media)+";"+str(tempo_video)+"\n")

            arquivo3.writelines(texto3)
            arquivo3.close()


    return img2 , persons, pid, old_frame,p0