#!/usr/bin/python3
# -*- coding: utf-8 -*-

# tokenize a file
def lex_file(filename):
    with open(filename, "r") as f:
        return [(filename, row, col, token ) for (row, line) in enumerate(f.readlines(), 1) for (col, token) in lex_line(line)]

#tokenize a line
def lex_line(line):
    tokens = line.split()
    coltok= [] 
    # to manage duplicated tokens in a line
    start = 0
    for token in tokens:
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token))
    return coltok

       
#print(lex_file("pgm1.porth"))

