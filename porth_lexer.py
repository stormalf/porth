#!/usr/bin/python3
# -*- coding: utf-8 -*-


#tokens digits and 3 operators for now
PLUS= "+"
MINUS = "-"
DUMP = "."
EQUAL = "="
OPIF = "IF"
OPEND = "END"
NUMBER= "number"
UNKNOWN= "unknown"

forbidden_tokens = [PLUS, MINUS, DUMP]

iota_counter= 0
error_counter = 0

def get_counter_error():
    return error_counter

# tokenize a file
def lex_file(filename):
    with open(filename, "r") as f:
        return [(filename, row, col, token_type, token ) for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(line)]

#tokenize a line
def lex_line(line):
    tokens = line.split()
    coltok= [] 
    # to manage duplicated tokens in a line
    start = 0
    for token in tokens:
        token_type = get_token_type(token)
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token_type, token))
    return coltok

#returns the type of the token
def get_token_type(token):
    if token == PLUS:
        return OP_ADD
    elif token == MINUS:
        return OP_SUB
    elif token == DUMP:
        return OP_DUMP
    elif token == EQUAL:
        return OP_EQUAL
    elif token == OPIF:
        return OP_IF
    elif token == OPEND:
        return OP_END
    else:       
        try:
            int(token)
            return OP_NUMBER
        except ValueError:
            return OP_UNKNOWN

#returns the label for the token type
def get_token_type_label(token):
    if token == OP_ADD:
        return PLUS
    elif token == OP_SUB:
        return MINUS
    elif token == OP_DUMP:
        return DUMP
    elif token == OP_EQUAL:
        return EQUAL
    elif token == OP_IF:
        return OPIF
    elif token == OP_END:
        return OPEND
    elif token == OP_NUMBER:
        return NUMBER
    elif token == OP_UNKNOWN:
        return UNKNOWN


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
OP_IF=iota()
OP_END=iota()
OP_NUMBER=iota()
OP_UNKNOWN=iota()
#keep in last line to have the counter working
COUNT_OPS=iota()

#error codes
NO_ERROR=iota(True)
ERR_TOK_UNKNOWN = iota()
ERR_TOK_FORBIDDEN = iota()
ERR_TOK_BLOCK = iota()


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

def opif():
    return (OP_IF,)

def opend():
    return (OP_END,)    

#returns the list of forbidden tokens as first token in a line (probably need to be removed if we accept multilines for a single instruction)
def check_first_token(token, forbidden_tokens):
    isOK = False
    if token in forbidden_tokens:
        isOK = True
    return isOK


#returns the function corresponding to the token found
def parse_word(token):
    global error_counter
    #print(word)
    filename, line, column, _, word = token
    if word == PLUS:
        return add()
    elif word == MINUS:
        return sub()
    elif word == DUMP:
        return dump()
    elif word == EQUAL:
        return equal() 
    elif word == OPIF:
        return opif()  
    elif word == OPEND:
        return opend()                              
    else:
        try :
            number = int(word)
            return push(number)                    
        except ValueError:
            print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            error_counter += 1
            return (None, None, None, None, None)

#returns the program in the porth language after two passes : first tokenize and second calculate cross references for IF/END
def load_program(filename):
    program, tokens, isOK = load_program_first_pass(filename)
    if isOK:
        program_xref = cross_reference_block(program, tokens)
    return program_xref, tokens, isOK

#do a first pass  to parse tokesn and check for errors
def load_program_first_pass(filename):
    global error_counter
    tokens = lex_file(filename)
    isOK = True
    current_line = 0
    first_token = False
    for token in tokens:
        filename, line, col, toktype, tok = token
        if line != current_line:
            first_token = True            
            current_line = line
        if check_first_token(tok, forbidden_tokens) and first_token:
            print(f"Error Code {ERR_TOK_FORBIDDEN} Token {tok} is forbidden in first position in file {filename}, line {line} column {col}, type token {get_token_type(toktype)}")
            error_counter += 1
            first_token = False
            isOK = False
        first_token = False    
    return [parse_word(word) for word in tokens], tokens, isOK

#cross references to store the link between a IF and this corresponding END operation!
def cross_reference_block(program, tokens):
    global error_counter
    stack = []
    iffound = False
    endfound = False
    for ip in range(len(program)):
        filename, line, col, *_ = tokens[ip]
        op = program[ip]
        if op[0] == OP_IF:
            stack.append(ip)
            iffound = True
        elif op[0] == OP_END:
            endfound = True
            if len(stack) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} END without IF at line {line} column {col}, in file {filename}")
                error_counter += 1
            else:
                if_ip = stack.pop()
                program[if_ip]= (OP_IF, ip)
    if iffound and not endfound:
        print(f"Error Code {ERR_TOK_BLOCK} IF without END at line {line}")
        error_counter += 1
    return program


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

def get_OP_IF():
    return OP_IF

def get_OP_END():
    return OP_END

# program, tokens, isOK = load_program("pgm6.porth")
# print(cross_reference_block(program, tokens))