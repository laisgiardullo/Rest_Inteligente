#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('Video_Intel.db')

with con:
    
    cur = con.cursor()
    cur.execute("CREATE TABLE Pessoa(Id INT, Status TEXT, Width INT, Instante_Inicial INT, Instante_Saida INT)")
    cur.execute("CREATE TABLE Posicao(Id INTEGER PRIMARY KEY AUTOINCREMENT, X INT, Y INT, Instante_Inicial INT, Instante_Final INT, Atual BOOLEAN, Pessoa_id INT, FOREIGN KEY(Pessoa_id) REFERENCES Pessoa(Id))")
    #cur.execute("INSERT INTO Pessoa VALUES(1,'Audi',52642)")
con.close