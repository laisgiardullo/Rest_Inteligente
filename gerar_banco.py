#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect(r'GUI\video_inteligente_gui\db.sqlite3')

with con:
    
    cur = con.cursor()
    #Timestamping
    cur.execute("CREATE TABLE DataHora(Id INTEGER PRIMARY KEY AUTOINCREMENT, Dia INT, Mes INT, Ano INT, Hora INT, Minutos INT, Segundos INT, Milissegundos INT)")
    
    #Matriz Imagem Automaticos
    #cur.execute("CREATE TABLE Pixel(Id INTEGER PRIMARY KEY AUTOINCREMENT, X INT, Y INT)")
    cur.execute("CREATE TABLE Quadrantes(Id INTEGER PRIMARY KEY AUTOINCREMENT, N_Quad_X INT, N_Quad_Y INT, X INT, Y INT, Width INT, Height INT, W_Pessoa INT, H_Pessoa INT)")
    
    #Pessoas, Posicao e Contorno
    cur.execute("CREATE TABLE Pessoa(Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)")
    cur.execute("CREATE TABLE Posicao(Id INTEGER PRIMARY KEY AUTOINCREMENT, X REAL, Y REAL, Instante_Inicial INT, Instante_Final INT, Atual INT, Pessoa_id INT, FOREIGN KEY(Pessoa_id) REFERENCES Pessoa(Id))")
    #cur.execute("CREATE TABLE Posicao(Id INTEGER PRIMARY KEY AUTOINCREMENT,Pixel_id INT, FOREIGN KEY(Pixel_id) REFERENCES Pixel(Id) , Instante_Inicial INT, Instante_Final INT, Atual INT, Pessoa_id INT, FOREIGN KEY(Pessoa_id) REFERENCES Pessoa(Id))")
    cur.execute("CREATE TABLE PontoAtualInterno(Id INTEGER PRIMARY KEY AUTOINCREMENT,EhContorno INT, X REAL, Y REAL, Pessoa_id INT, FOREIGN KEY(Pessoa_id) REFERENCES Pessoa(Id))")

    #Calibracao do Usuario
    cur.execute("CREATE TABLE MedidaParcial(Id INTEGER PRIMARY KEY AUTOINCREMENT, X INT, Y INT, Width INT, Height INT, Quadranteid INT, FOREIGN KEY(Quadranteid) REFERENCES Quadrante(Id))")
    cur.execute("CREATE TABLE Local(Id INTEGER PRIMARY KEY AUTOINCREMENT, Nome INT, Tipo TEXT, X INT, Y INT, Width INT, Height INT)") #tipo = tracking, fila ou ignorar
    
    #Calculos
    #medida por quadrante
    cur.execute("CREATE TABLE MedidaFinal(Id INTEGER PRIMARY KEY AUTOINCREMENT, Width INT, Height INT, Quadranteid INT, FOREIGN KEY(Quadranteid) REFERENCES Quadrante(Id))")
    #numero de pessoas
    cur.execute("CREATE TABLE NumeroPessoasQuadrante(Id INTEGER PRIMARY KEY AUTOINCREMENT, Num_de_Pessoas INT, DataHora_id INT, Quadranteid INT, FOREIGN KEY(DataHora_id) REFERENCES DataHora(Id), FOREIGN KEY(Quadranteid) REFERENCES Quadrante(Id))")
    cur.execute("CREATE TABLE NumeroPessoasLocal(Id INTEGER PRIMARY KEY AUTOINCREMENT, Num_de_Pessoas INT, DataHora_id INT, Local_id INT, FOREIGN KEY(DataHora_id) REFERENCES DataHora(Id), FOREIGN KEY(Local_id) REFERENCES Local(Id))")
    cur.execute("CREATE TABLE NumeroPessoasTotal(Id INTEGER PRIMARY KEY AUTOINCREMENT, Num_de_Pessoas INT, DataHora_id INT, FOREIGN KEY(DataHora_id) REFERENCES DataHora(Id))")

    #cur.execute("CREATE TABLE Estabelecimento(Id INTEGER PRIMARY KEY AUTOINCREMENT, Nome TEXT, Faturamento_Mensal INT, Cidade TEXT, Telefone INT)")
con.commit()
con.close