#!/usr/bin/python3
# -*- coding: utf-8 -*-

from porth_globals import * 


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
        return [{'loc': (filename, row, col), 'type': token_type, 'value': token } for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(line)]

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
    filename, line, column = token['loc']
    word = token['value']
    loc = (filename, line, column)
    if word == PLUS:
        return {'type': OP_ADD,  'loc': loc, 'value': None, 'jmp': None}
    elif word == MINUS:
        return {'type': OP_SUB, 'loc': loc, 'value': None, 'jmp': None}
    elif word == DUMP:
        return {'type': OP_DUMP, 'loc': loc , 'value': None, 'jmp': None}
    elif word == EQUAL:
        return {'type': OP_EQUAL, 'loc': loc, 'value': None, 'jmp': None} 
    elif word == OPIF:
        return {'type': OP_IF, 'loc': loc, 'value': None, 'jmp': None}  
    elif word == OPEND:
        return {'type': OP_END, 'loc': loc, 'value': None, 'jmp': None} 
    elif word == OPELSE:
        return {'type': OP_ELSE, 'loc': loc, 'value': None, 'jmp': None} 
    elif word == OPDUP:
        return {'type': OP_DUP, 'loc': loc, 'value': None, 'jmp': None}  
    elif word == OPDUP2:
        return {'type': OP_DUP2, 'loc': loc, 'value': None, 'jmp': None}                                                             
    elif word == OPGT:
        return {'type': OP_GT, 'loc': loc, 'value': None, 'jmp': None}          
    elif word == OPLT:
        return {'type': OP_LT, 'loc': loc, 'value': None, 'jmp': None}   
    elif word == OPGE:
        return {'type': OP_GE, 'loc': loc, 'value': None, 'jmp': None}   
    elif word == OPLE:
        return {'type': OP_LE, 'loc': loc, 'value': None, 'jmp': None}                   
    elif word == OPNE:
        return {'type': OP_NE, 'loc': loc, 'value': None, 'jmp': None}    
    elif word == OPDIV:
        return {'type': OP_DIV, 'loc': loc, 'value': None, 'jmp': None}  
    elif word == OPMUL:
        return {'type': OP_MUL, 'loc': loc, 'value': None, 'jmp': None}                                
    elif word == OPWHILE:
        return {'type': OP_WHILE, 'loc': loc, 'value': None, 'jmp': None}
    elif word == OPDO:
        return {'type': OP_DO, 'loc': loc, 'value': None, 'jmp': None} 
    elif word == OPMEM:
        return {'type': OP_MEM, 'loc': loc, 'value': None, 'jmp': None}                                     
    elif word == OPLOAD:
        return {'type': OP_LOAD, 'loc': loc, 'value': None, 'jmp': None}  
    elif word == OPSTORE:
        return {'type': OP_STORE, 'loc': loc, 'value': None, 'jmp': None}    
    elif word == OPSYSCALL1:
        return {'type': OP_SYSCALL1, 'loc': loc, 'value': None, 'jmp': None}           
    elif word == OPSYSCALL2:
        return {'type': OP_SYSCALL2, 'loc': loc, 'value': None, 'jmp': None}           
    elif word == OPSYSCALL3:
        return {'type': OP_SYSCALL3, 'loc': loc, 'value': None, 'jmp': None}                          
    elif word == OPSYSCALL4:
        return {'type': OP_SYSCALL4, 'loc': loc, 'value': None, 'jmp': None}   
    elif word == OPSYSCALL5:
        return {'type': OP_SYSCALL5, 'loc': loc, 'value': None, 'jmp': None}   
    elif word == OPSYSCALL6:
        return {'type': OP_SYSCALL6, 'loc': loc, 'value': None, 'jmp': None}                           
    elif word == OPRETURN:
        return {'type': OP_RETURN, 'loc': loc, 'value': None, 'jmp': None} 
    elif word == OPSWAP:
        return {'type': OP_SWAP, 'loc': loc, 'value': None, 'jmp': None}   
    elif word == OPDROP:
        return {'type': OP_DROP, 'loc': loc, 'value': None, 'jmp': None}    
    elif word == OPSHL:
        return {'type': OP_SHL, 'loc': loc, 'value': None, 'jmp': None}    
    elif word == OPSHR:
        return {'type': OP_SHR, 'loc': loc, 'value': None, 'jmp': None}
    elif word == OPORB:
        return {'type': OP_ORB, 'loc': loc, 'value': None, 'jmp': None}
    elif word == OPANDB:
        return {'type': OP_ANDB, 'loc': loc, 'value': None, 'jmp': None}
    elif word == OPOVER:
        return {'type': OP_OVER, 'loc': loc, 'value': None, 'jmp': None}
    elif word == OPMOD:
        return {'type': OP_MOD, 'loc': loc, 'value': None, 'jmp': None}
    else:
        try :
            number = int(word)
            return {'type': OP_PUSH, 'loc': loc, 'value': number,  'jmp': None}                    
        except ValueError:
            print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            error_counter += 1
            return {'type': None, 'loc': None, 'value': None, 'jmp': None}

#returns the program in the porth language after two passes : first tokenize and second calculate cross references for IF/END
def load_program(filename):
    program, tokens, isOK = load_program_first_pass(filename)
    program_xref = program
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
        filename, line, col = token['loc']
        toktype = token['type']
        tok = token['value']
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
        loc = (filename, line, col)
        op = program[ip]
        if op['type'] == OP_IF:
            #print(f"IF {ip} {op}")
            stack.append(ip)
            ifarray.append(ip)
        elif op['type'] == OP_ELSE:    
            #print(f"ELSE {ip} {op}")        
            if len(ifarray) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} ELSE without IF in file {filename}, line {line} column {col}")
                error_counter += 1
            else:
                if_ip = stack.pop()
                program[if_ip]['jmp'] = ip + 1
                stack.append(ip)   
        elif op['type'] == OP_END:
            #print(f"END {ip} {op}")
            if len(ifarray) == 0 :
                print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                error_counter += 1
            else:
                ifarray.pop()
                block_ip = stack.pop()
                if program[block_ip]['type'] == OP_IF or program[block_ip]['type'] == OP_ELSE:
                    program[block_ip]['jmp'] =  ip
                    program[ip]['jmp'] = ip + 1
                elif program[block_ip]['type'] == OP_DO:
                    program[ip]['jmp'] = program[block_ip]['jmp']
                    program[block_ip]['jmp'] = ip + 1
                else:
                    print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                    error_counter += 1
        elif op['type'] == OP_WHILE:
            #print(f"DO {ip} {op}")
            stack.append(ip)
        elif op['type'] == OP_DO:
            ifarray.append(ip)
            #print(f"DO {ip} {op}")
            if len(stack) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} DO without WHILE in file {filename}, line {line} column {col}")
                error_counter += 1
            else:
                while_ip = stack.pop()
                program[ip]['jmp'] = while_ip
                stack.append(ip)
    if len(ifarray) > 0:
        print(f"Error Code {ERR_TOK_BLOCK} IF ELSE END missing one")
        error_counter += 1
    if error_counter > 0:
        print(f"{error_counter} errors found during cross references")        
        error= True
    return program, error
