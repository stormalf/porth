#!/usr/bin/python3
# -*- coding: utf-8 -*-


#tokens digits and 3 operators for now
PLUS= "+"
MINUS = "-"
DUMP = "."
EQUAL = "="
OPIF = "IF"
OPEND = "END"
OPELSE= "ELSE"
NUMBER= "number"
UNKNOWN= "unknown"
OPDUP="DUP"
OPGT = ">"
OPLT = "<"
OPWHILE = "WHILE"
OPDO = "DO"

LABEL_PLUS= "PLUS"
LABEL_MINUS= "MINUS"
LABEL_DUMP= "PRINT"
LABEL_EQUAL= "EQUAL"
LABEL_IF= "IF"
LABEL_ELSE= "ELSE"
LABEL_END= "END"
LABEL_NUMBER = "NUMBER"
LABEL_UNKNOWN = "UNKNOWN"
LABEL_DUP="DUPLICATE"
LABEL_GT= "GREATER"
LABEL_LT= "LESSER"
LABEL_WHILE= "WHILE"
LABEL_DO= "DO"

forbidden_tokens = [PLUS, MINUS, DUMP]

#list of comments types probably I'll prefer the python comment syntax for myself
COMMENTS = ["//", "#", ";"]

iota_counter= 0
error_counter = 0

def get_counter_error():
    return error_counter

#to manage list of comments types and not only one type of comment
def split(txt, seps):
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


# tokenize a file
def lex_file(filename):
    with open(filename, "r") as f:
        return [(filename, row, col, token_type, token ) for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(line)]

#tokenize a line
def lex_line(line):
    linewithoutcomments = split(line, COMMENTS)
    tokens = linewithoutcomments[0].split()
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
    elif token == OPELSE:
        return OP_ELSE        
    elif token == OPDUP:
        return OP_DUP     
    elif token == OPGT:
        return OP_GT          
    elif token == OPLT:
        return OP_LT    
    elif token == OPWHILE:
        return OP_WHILE   
    elif token == OPDO:
        return OP_DO                           
    else:       
        try:
            int(token)
            return OP_NUMBER
        except ValueError:
            return OP_UNKNOWN

#returns the label for the token type
def get_token_type_label(tokentype):
    if tokentype == OP_ADD:
        return LABEL_PLUS
    elif tokentype == OP_SUB:
        return LABEL_MINUS
    elif tokentype == OP_DUMP:
        return LABEL_DUMP
    elif tokentype == OP_EQUAL:
        return LABEL_EQUAL
    elif tokentype == OP_IF:
        return LABEL_IF
    elif tokentype == OP_END:
        return LABEL_END
    elif tokentype == OP_ELSE:
        return LABEL_ELSE        
    elif tokentype == OP_NUMBER:
        return LABEL_NUMBER
    elif tokentype == OP_UNKNOWN:
        return LABEL_UNKNOWN
    elif tokentype == OP_DUP:
        return LABEL_DUP
    elif tokentype == OP_GT:
        return LABEL_GT        
    elif tokentype == OP_LT:
        return LABEL_LT   
    elif tokentype == OP_WHILE:
        return LABEL_WHILE
    elif tokentype == OP_DO:
        return LABEL_DO

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
OP_ELSE=iota()
OP_NUMBER=iota()
OP_UNKNOWN=iota()
OP_DUP=iota()
OP_GT=iota()
OP_LT=iota()
OP_WHILE=iota()
OP_DO=iota()
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

def opelse():
    return (OP_ELSE,)    

def opdup():
    return (OP_DUP,)    

def opgt():
    return (OP_GT,)    

def oplt():
    return (OP_LT,)    

def opwhile():
    return (OP_WHILE,)    

def opdo():
    return (OP_DO,)   

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
    elif word == OPELSE:
        return opelse() 
    elif word == OPDUP:
        return opdup()                                                    
    elif word == OPGT:
        return opgt()          
    elif word == OPLT:
        return oplt()   
    elif word == OPWHILE:
        return opwhile() 
    elif word == OPDO:
        return opdo()                           
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
        program_xref, error = cross_reference_block(program, tokens)
        if error:
            isOK = False
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
    ifarray= []
    error = False
    for ip in range(len(program)):
        #print(stack)
        filename, line, col, *_ = tokens[ip]
        op = program[ip]
        if op[0] == OP_IF:
            #print(f"IF {ip} {op}")
            stack.append(ip)
            ifarray.append(ip)
        elif op[0] == OP_ELSE:    
            #print(f"ELSE {ip} {op}")        
            if len(ifarray) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} ELSE without IF in file {filename}, line {line} column {col}")
                error_counter += 1
            else:
                if_ip = stack.pop()
                program[if_ip] = (OP_IF, ip + 1)
                stack.append(ip)   
        elif op[0] == OP_END:
            #print(f"END {ip} {op}")
            if len(ifarray) == 0 :
                print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                error_counter += 1
            else:
                ifarray.pop()
                block_ip = stack.pop()
                if program[block_ip][0] == OP_IF or program[block_ip][0] == OP_ELSE:
                    program[block_ip] = (program[block_ip][0], ip)
                    program[ip] = (OP_END, ip + 1)
                elif program[block_ip][0] == OP_DO:
                    program[ip] = (OP_END, program[block_ip][1])
                    program[block_ip] = (OP_DO, ip + 1)
                else:
                    print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                    error_counter += 1
        elif op[0] == OP_WHILE:
            #print(f"DO {ip} {op}")
            stack.append(ip)
        elif op[0] == OP_DO:
            ifarray.append(ip)
            #print(f"DO {ip} {op}")
            if len(stack) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} DO without WHILE in file {filename}, line {line} column {col}")
                error_counter += 1
            else:
                while_ip = stack.pop()
                program[ip] = (OP_DO, while_ip)
                stack.append(ip)
    if len(ifarray) > 0:
        print(f"Error Code {ERR_TOK_BLOCK} IF ELSE END missing one")
        error_counter += 1
    if error_counter > 0:
        print(f"{error_counter} errors found during cross references")        
        error= True
    return program, error


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

def get_OP_ELSE():
    return OP_ELSE

def get_OP_DUP():
    return OP_DUP

def get_OP_GT():
    return OP_GT

def get_OP_LT():
    return OP_LT

def get_OP_WHILE():
    return OP_WHILE

def get_OP_DO():
    return OP_DO

def print_ast(ast):
    print("----------------------------------")
    print('------------ AST TREE ------------')
    print("----------------------------------")
    #print(OP_PUSH, OP_ADD, OP_SUB, OP_DUMP, OP_EQUAL, OP_IF, OP_END, OP_ELSE)
    indent = 0
    for *_, tokentype, token in ast:
        tokenlabel = get_token_type_label(tokentype)
        print(tokenlabel, token)        
        if tokentype == OP_IF:
            print("if-body")
            indent += 2
        if tokentype == OP_DO:
            print("do-body")
            indent += 2            
        elif tokentype == OP_ELSE:
            print("else-body")
        elif tokentype == OP_END:
            print("end-body")
            indent -= 2
        for i in range(indent):
            print(" ", end="")
    print("----------------------------------")



# program, tokens, isOK = load_program("pgm8.porth")
# print(cross_reference_block(program, tokens))
# print_ast(tokens)