#!/usr/bin/python3
# -*- coding: utf-8 -*-


#tokens digits and 3 operators for now
PLUS= "+"
MINUS = "-"
DUMP = "."
EQUAL = "="

forbidden_tokens = [PLUS, MINUS, DUMP]

iota_counter= 0
error_counter = 0

def get_counter_error():
    return error_counter

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


#enum function in python 
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter=0
    else:
        iota_counter+=1
    return iota_counter

OP_PUSH=iota(True)    
OP_ADD=iota()
OP_SUB=iota()
OP_DUMP=iota()
OP_EQUAL=iota()
#keep in last line to have the counter working
COUNT_OPS=iota()

NO_ERROR=iota(True)
ERR_TOK_UNKNOWN = iota()
ERR_TOK_FORBIDDEN = iota()


##functions for the porth language
def push(value):
    return (OP_PUSH, value)

def add():
    return (OP_ADD,)

def sub():
    return (OP_SUB,)

def dump():
    return (OP_DUMP,)

def equal():
    return (OP_EQUAL,)

def check_first_token(token, forbidden_tokens):
    isOK = False
    if token in forbidden_tokens:
        isOK = True
    return isOK


#returns the function corresponding to the token found
def parse_word(token):
    global error_counter
    #print(word)
    filename, line, column, word = token

    if word == PLUS:
        return add()
    elif word == MINUS:
        return sub()
    elif word == DUMP:
        return dump()
    elif word == EQUAL:
        return equal()        
    else:
        try :
            number = int(word)
            return push(number)                    
        except ValueError:
            print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            error_counter += 1
            return (None, None, None, None)

#returns the program in the porth language
def load_program(filename):
    global error_counter
    tokens = lex_file(filename)
    isOK = True
    current_line = 0
    first_token = False
    for token in tokens:
        filename, line, col, tok = token
        if line != current_line:
            first_token = True            
            current_line = line
        if check_first_token(tok, forbidden_tokens) and first_token:
            print(f"Error Code {ERR_TOK_FORBIDDEN} Token {tok} is forbidden in first position in file {filename}, line {line} column {col}")
            error_counter += 1
            first_token = False
            isOK = False
        first_token = False    

    return [parse_word(word) for word in tokens], tokens, isOK
 

def get_OPS():
    return COUNT_OPS    

def get_OP_PUSH():
    return OP_PUSH

def get_OP_ADD():
    return OP_ADD
    
def get_OP_SUB():
    return OP_SUB

def get_OP_DUMP():
    return OP_DUMP

def get_OP_EQUAL():
    return OP_EQUAL


