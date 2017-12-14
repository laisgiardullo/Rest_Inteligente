def Pessoa_Nova(cx, new_width, cy, cur, tempo_video):
    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (cx, cx, cy, cy,))
    quadrante = cur.fetchall()
    Quadranteid = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid=?""", (Quadranteid,))
    medida = (cur.fetchall())[0]
    #xa = medida[1]
    #ya = medida[2]
    xa = largura_padrao
    ya = altura_padrao


    limite = xa*xa+ya*ya
    cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X)+(?-Y)*(?-Y))<=? AND Atual=1 AND Instante_Inicial!=? ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y))""", (cx, cx, cy, cy, limite, tempo_video, cx, cx, cy, cy, ))
    
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


def Pessoa_Nova3(cx, new_width, cy, cur, tempo_video, cnt, h, new_x, y):
    novo = True
    id_pessoa= None
    id_posicao=None

    cur.execute("""SELECT * FROM 'Quadrantes' WHERE (X<=? AND X+Width>=? AND Y<=? AND Y+Height>=?)""", (cx, cx, cy, cy,))
    quadrante = cur.fetchall()
    Quadranteid = quadrante[0][0]
    cur.execute("""SELECT * FROM 'MedidaFinal' WHERE Quadranteid=?""", (Quadranteid,))
    medida = (cur.fetchall())[0]
    xa = medida[1]
    ya = medida[2]
    limite = xa*xa+ya*ya
    cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X)+(?-Y)*(?-Y))<=? AND Atual=1 AND Instante_Inicial!=? ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y))""", (cx, cx, cy, cy, limite, tempo_video, cx, cx, cy, cy, ))
    
    #cur.execute("""SELECT * FROM 'Posicao' WHERE ((abs(?-X)<? OR abs(?-Y)<120) AND Atual=1) ORDER BY abs(?-X)""", (cx, new_width, cy, cx ))
    lista = cur.fetchall()
    print(len(lista))
    if (len(lista)>0):
        #print("eh velho")
        id_pessoa= lista[0][6]
        id_posicao=lista[0][0]
        novo = False
    else:
        for i in range (new_width):
            for j in range (h):
                if (novo):
                    no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
                    if (novo and no_contorno>=0):
                        x_salvar = new_x+i
                        y_salvar = y+j
                        cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X-1<? AND X+1>? AND Y-1<? AND Y+1>?""", (x_salvar,x_salvar,y_salvar,y_salvar,))
                        lista_pontos = cur.fetchall()
                        if (len(lista_pontos)!=0):
                            novo = False
                            id_pessoa = lista_pontos[0][4]
                            cur.execute("""SELECT * FROM 'Posicao' WHERE Pessoa_id = ?""", (id_pessoa,))
                            id_posicao = (cur.fetchall())[0][0]
                i+3
                j+3


    return (novo, id_pessoa, id_posicao)



def Pessoa_Nova2(new_width, h, cnt, pid, new_x, y, cur, lista_pontosinternos, limitex, limitey):
    print("pessoa nova2")
    lista_objetos = []
    novo = True
    lista_pontos = []
    id_pessoa = None
    #xa, ya = Media_Medidas(new_x+new_width/2, y+h/2, cur)
    #ya = Altura_Media(new_x+new_width/2, y+h/2, cur)
    #xa = largura_padrao
    #ya = altura_padrao
    achou_proximo = False

    #limite = xa*xa+ya*ya
    i=0
    j=0
    while (i < new_width):
        while (j< h):
    #for i in range (new_width):
    #    for j in range (h):
            achou_existente = False
            no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
            
            if (no_contorno>0): #se estiver dentro do contorno
                
                x_salvar = new_x+i
                y_salvar = y+j
                cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X-1<? AND X+1>? AND Y-1<? AND Y+1>?""", (x_salvar,x_salvar,y_salvar,y_salvar))
                lista_pontos = cur.fetchall()
                if (len(lista_pontos)>0):
                    achou_existente = True
                if (achou_existente and novo):
                    novo = False
                    id_pessoa = lista_pontos[0][4]
                if (achou_existente==False):
                    cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X))<=? AND ((?-Y)*(?-Y))<=? AND Atual=1 ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y)) ASC""", (x_salvar, x_salvar, limitex, y_salvar, y_salvar, limitey, x_salvar, x_salvar, y_salvar, y_salvar, ))
                    #cur.execute("""SELECT * FROM 'Posicao' WHERE ((?-X)*(?-X)+(?-Y)*(?-Y))<=? AND Atual=1 ORDER BY ((?-X)*(?-X)+(?-Y)*(?-Y)) ASC""", (x_salvar, x_salvar, y_salvar, y_salvar, limite, x_salvar, x_salvar, y_salvar, y_salvar, ))
                    lista_posprox = cur.fetchall()
                    if (len(lista_posprox)!=0 and novo==True):
                        achou_proximo = True
                        novo = False
                        id_pessoa = lista_posprox[0][6]
                    #cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X-5<? AND X+5>? AND Y-5<? AND Y+5>?""", (x_salvar,x_salvar,y_salvar,y_salvar))
                #elif (not achou_existente):
                    #x_salvar = new_x+i
                    #y_salvar = y+j
                    #if (no_contorno==0):
                    #    lista_objetos.append([None, 1, x_salvar,y_salvar, pid])
                    if (no_contorno>0):
                        lista_objetos.append([None, 0, x_salvar,y_salvar, pid, None])
            j+=8
        j=0
        i+=8
    if (novo == False):
        for obj in lista_objetos:
            obj[4] = id_pessoa
    for objeto in lista_objetos:
        lista_pontosinternos.append(objeto)


    #cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?)", lista_objetos)
    return (novo, id_pessoa, lista_pontosinternos)

def Determinar_Pessoa(contours1, img, areaTH, pid, num_frame, tempo_video, novos_pts, con, tipo_seguir):
     ### XX OUTROS TESTES XX ###
    #_, contours0, hierarchy = cv2.findContours(teste2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ### XX OUTROS TESTES XX ###

    #num_contorno = 0
    #lista_width = []
    #texto4.append(str(contours1))
    #print (contours1)
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left

        largura_media = Largura_Media(x,y, cur)
        if (area>areaTH):
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            #lista_width.append(new_width)
            if(tipo_seguir == 1):
                pid = Salvar_Mostrar_PessoaMet1(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, con)
                novos_pts = []
            elif(tipo_seguir == 2):
                pid, novos_pts = Salvar_Mostrar_PessoaPontual(img, pid, pp, x, y, h, new_width, num_frame,tempo_video, novos_pts,con)

    return img , pid, novos_pts


def Comparar_e_Salvar_Novos(contours1, img, areaTH, pid, num_frame, tempo_video, con):
    cur = con.cursor()
    for cnt in contours1:
        cv2.drawContours(img, cnt, -1, (0,255,0), 0, 8)
        area = cv2.contourArea(cnt)
        
        #########   LINK   ###########
        #ver http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        x,y,w,h = cv2.boundingRect(cnt) # x e y: top left

        largura_media = Largura_Media(x,y, cur)
        if (area>areaTH):
            pp = Qnt_Pessoas_Contorno(w, largura_media)
            new_width = w/pp #calcular a nova largura de somente 1 pessoa
            it = 0 #it = iteracao
            lista_obj = []
            lista_obj_pos = []
            cur = con.cursor()
            for i in range (pp):
                novo = True
                new_x, cx, cy = Atualizar_Retangulo(x, y, h, new_width, it)
                novo, pessoax, posicaox = Pessoa_Nova(cx, new_width, cy, cur, tempo_video)
                it+=new_width
                #novo, pessoax, posicaox = Pessoa_Nova3(cx, new_width, cy, cur, tempo_video, cnt, h, new_x, y)
                if (novo and cx>largura_padrao and cx<(w_frame-largura_padrao) and cy>altura_padrao and cy<(h_frame-altura_padrao)):
                    #print ("sounovo")
                    #p = Person.Pessoa_Pontual(pid,cx,cy, new_width, num_frame,tempo_video)
                    #(Id INT, X INT, Y INT, Status TEXT, Width INT, Num_Frame INT, Instante INT)")
                    #obj_pessoa = (Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)

                    lista_obj.append((pid,'in',new_width,tempo_video, None))
                    lista_obj_pos.append((None, cx, cy, tempo_video, None, 1, pid))
                    Salvar_PontoAtualInterno(new_width, h, cnt, pid, new_x, y, cur)
                    pid += 1
                    #########   EXPLICACAO LOGICA   ###########
                    ##agora, vamos fazer um teste: desenhar retangulo em cada objeto
                    img = cv2.rectangle(img,(new_x,y),(new_x+new_width,y+h),(0,255,0),2)
                    
                    #pa = np.array ([[cx]])
                    #pb = np.array ([[cy]])
                    #nv_pt = np.dstack((pa,pb))
                    #nv_pt = nv_pt.astype(np.float32)
                    #if (num_frame>20): #so comeca a guardar depois do 21 que eh quando estabiliza o background
                    #    if (novos_pts !=[]):
                    #        novos_pts = np.append(novos_pts,nv_pt, axis = 0)
                    #    else: novos_pts = nv_pt
                    if (lista_obj!=[]):
                        with con:
                            cur = con.cursor()
                            cur.executemany("INSERT INTO Pessoa VALUES(?,?,?,?,?)", lista_obj)
                            cur.executemany("INSERT INTO Posicao VALUES(?,?,?,?,?,?,?)", lista_obj_pos)
                            lista_obj=[]
                            lista_obj_pos=[]
                    else:
                        #Adicionar_Pontos_Contorno(new_width, h, cnt, pessoax, new_x, y ,cur)
                        pass


    return img , pid



    ###APOIO DETECCAO

    def Salvar_PontoAtualInterno(new_width, h, cnt, pid, new_x, y, cur):
    lista_objetos = []
    for i in range (new_width):
        for j in range (h):
            no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
            if (no_contorno>=0):
                x_salvar = new_x+i
                y_salvar = y+j
                if (no_contorno==0):
                    lista_objetos.append((None, 1, x_salvar,y_salvar, pid, None))
                if (no_contorno>0):
                    lista_objetos.append((None, 0, x_salvar,y_salvar, pid, None))
                j+=1
                i+=1
    cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", lista_objetos)
    return

def Adicionar_Pontos_Contorno(new_width, h, cnt, pessoax, new_x, y ,cur):
    lista_objetos = []
    for i in range (new_width):
        for j in range (h):
            no_contorno = cv2.pointPolygonTest(cnt, (new_x+i, y+j), False)
            x_salvar = new_x+i
            y_salvar = y+j
            if (no_contorno>=0):
                cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE X = ? AND Y=? AND Pessoa_id=?""", (x_salvar, y_salvar, pessoax,))
                lista_ponto = cur.fetchall()
                if(len(lista_ponto)==0):
                    if (no_contorno==0):
                        lista_objetos.append((None, 1, x_salvar,y_salvar, pessoax, None))
                    if (no_contorno>0):
                        lista_objetos.append((None, 0, x_salvar,y_salvar, pessoax, None))
            j+=3
            i+=3
    cur.executemany("INSERT INTO PontoAtualInterno VALUES(?,?,?,?,?,?)", lista_objetos)
    return



##POSICIONAMENTO

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


def Limpar_PontosPerdidos(cur, matriz_flow):
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


def Limpar_PontosPerdidos2(cur, matriz_flow):
    cur.execute("""SELECT * FROM 'Posicao' WHERE Atual =1""")
    lista_pos = cur.fetchall()
    for pos in lista_pos:
        pessoa_id = pos[6]
        x_pos = pos[1]
        y_pos = pos[2]
        largura_media, altura_media= Medidas_Media(x_pos, y_pos, cur)
        dist_quad_max = largura_media*largura_media + altura_media*altura_media
        cur.execute("""SELECT * FROM 'PontoAtualInterno' WHERE Pessoa_id=?""", (pessoa_id,))
        lista_pontos = cur.fetchall()
        for ponto in lista_pontos:
            x_ponto=ponto[2]
            y_ponto=ponto[3]
            id_ponto = ponto[0]
            dist_quad_x = (x_pos-x_ponto)*(x_pos-x_ponto)
            dist_quad_y = (y_pos-y_ponto)*(y_pos-y_ponto)
            if((dist_quad_y+dist_quad_x)>=dist_quad_max):
                
                # deslocamento_x = int(matriz_flow[int(y_ponto)][int(x_ponto)][0])
                # deslocamento_y = int(matriz_flow[int(y_ponto)][int(x_ponto)][1])
                # if (deslocamento_x==0 and deslocamento_y==0):
                #   cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Id=?""",(id_ponto,))

                 for ponto_final in lista_pontos:
                    ponto_final_x = ponto_final[2]
                    ponto_final_y = ponto_final[3]
                    deslocamento_x = int(matriz_flow[int(ponto_final_y)][int(ponto_final_x)][0])
                    deslocamento_y = int(matriz_flow[int(ponto_final_y)][int(ponto_final_x)][1])
                    if (deslocamento_x==0 and deslocamento_y==0):
                        cur.execute("""DELETE FROM 'PontoAtualInterno' WHERE Id=?""",(ponto_final[0],))
    return




def Limpar_PtosAreasDescarte1(cur, tempo_video):
    cur.execute("""SELECT * FROM 'Local' WHERE Tipo ='ignorar'""")
    locais_ign = cur.fetchall()
    for local in locais_ign:
        local_x = local[3]
        local_y = local[4]
        local_x_max = local_x + local[5]
        local_y_max = local_y + local[6]
        cur.execute("""SELECT * FROM 'Posicao' WHERE Atual = 1 AND X>=? AND X<=? AND Y>=? AND Y<=?""", (local_x, local_x_max, local_y, local_y_max,))
        lista_pontos_excluir = cur.fetchall()
        for ponto in lista_pontos_excluir:
            id_pessoa = ponto[6]
            PessoaSair(cur, id_pessoa, tempo_video)
    return
        #cur.execute("CREATE TABLE Local(Id INTEGER PRIMARY KEY AUTOINCREMENT, Nome INT, Tipo TEXT, X INT, Y INT, Width INT, Height INT)") #tipo = tracking, fila ou ignorar
