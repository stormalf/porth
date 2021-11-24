#!/usr/bin/python3
# -*- coding: utf-8 -*-

from porth_globals import * 

error_counter = 0
def get_counter_error():
    global error_counter
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
        return [{'loc': (filename, row, col), 'type': token_type, 'value': token } for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(row, line)]


#separate a line into strings and non strings, calculate the start and end of each token and returns the list of tokens
#line here represents a subset(without comments) of the line
#probably to improve this part later
def separate_line(startline, line, sep):
    strings = []
    notstrings = []
    start = 0
    end = 0
    for i in range(len(line)):
        if line[i] == sep:
            if start == 0:
                start = i + 1 
            else:
                end = i
                strings.append((startline + start, OP_STRING, line[start:end]))
                start = 0
                end = 0
    #remove the strings from the line to parse the rest as tokens
    for (*_, string) in strings:
        notstrings.extend(line.replace(string, '').replace(DOUBLE_QUOTE, '').split())
    return strings, notstrings

#returns the list of tokens for non strings tokens, here line is the line of the original file
def parse_not_string(line, tokens):
    start = 0
    coltok= []
    for token in tokens:
        token_type = get_token_type(token)
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token_type, token)) 
    return coltok


#tokenize a line. Ignore comments Not that you can't use Detects if double quotes to parse strings
def lex_line(row, line):
    global error_counter
    coltok= [] 
    strings= []
    linewithoutcomments = split(line, COMMENTS)
    startline= line.find(linewithoutcomments[0]) + 1
    if linewithoutcomments[0].count(DOUBLE_QUOTE) % 2 != 0:
        print(f"Error Code {ERR_TOK_STRING} Unbalanced quotes in line {row} ")
        error_counter += 1
        isOK = False
        return coltok
    if DOUBLE_QUOTE in line:
        stringline = linewithoutcomments[0] 
        #print(stringline)
        strings, notstrings= separate_line(startline, stringline, DOUBLE_QUOTE)
        #print(strings, notstrings)
        coltok.extend(strings)
        if len(notstrings) == 0:
            return coltok
        for i, _ in enumerate(notstrings):
            tokens = notstrings[i].split()
            notstrings_result = parse_not_string(line, tokens)
            coltok.append(notstrings_result[0])
    else:
        tokens = linewithoutcomments[0].split()
        token_not_string = parse_not_string(line, tokens)
        coltok.extend(token_not_string)
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
    filename, line, column = token['loc']
    word = token['value']
    tokentype = token['type']
    loc = (filename, line, column)
    if word in keyword_table:
        return {'type': keyword_table[word], 'loc': token['loc'], 'value': word, 'jmp': None}
    elif tokentype==OP_STRING:
        return {'type': tokentype, 'value': str(bytes(word, "utf-8").decode("unicode_escape")), 'loc': token['loc']}
    else:
        try :
            number = int(word)
            return {'type': OP_PUSH, 'loc': loc, 'value': number,  'jmp': None}                    
        except ValueError:
            print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            error_counter += 1
            return {'type': OP_UNKNOWN, 'loc': (filename, line, column), 'value': word, 'jmp': None}


#returns the program in the porth language after two passes : first tokenize and second calculate cross references for IF/END
def load_program(filename):
    program, tokens, isOK = load_program_first_pass(filename)
    program_xref = program
    if isOK:
        program_xref, error = cross_reference_block(program, tokens)
        if error:
            isOK = False
    return program_xref, tokens, isOK


#do a first pass  to parse tokens and check for errors
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
    error_xrefs = 0
    stack = []
    ifarray= []
    error = False
    for ip in range(len(program)):
        filename, line, col, *_ = tokens[ip]
        loc = (filename, line, col)
        op = program[ip]
        if op['type'] == OP_IF:
            stack.append(ip)
            ifarray.append(ip)
        elif op['type'] == OP_ELSE:    
            if len(ifarray) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} ELSE without IF in file {filename}, line {line} column {col}")
                error_xrefs += 1
            else:
                if_ip = stack.pop()
                program[if_ip]['jmp'] = ip + 1
                stack.append(ip)   
        elif op['type'] == OP_END:
            if len(ifarray) == 0 :
                print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                error_xrefs += 1
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
                    error_xrefs += 1
        elif op['type'] == OP_WHILE:
            stack.append(ip)
        elif op['type'] == OP_DO:
            ifarray.append(ip)
            if len(stack) == 0:
                print(f"Error Code {ERR_TOK_BLOCK} DO without WHILE in file {filename}, line {line} column {col}")
                error_xrefs += 1
            else:
                while_ip = stack.pop()
                program[ip]['jmp'] = while_ip
                stack.append(ip)
    if len(ifarray) > 0:
        print(f"Error Code {ERR_TOK_BLOCK} IF ELSE END missing one")
        error_xrefs += 1
    if error_xrefs > 0:
        print(f"{error_xrefs} errors found during cross references")  
        error_counter = error_counter + error_xrefs      
        error= True
    return program, error


#program, tokens, isOK = load_program("pgm6.porth")
#print(cross_reference_block(program, tokens)) 
# with open("tests/string1.porth", "r") as f:
#     for i, line in enumerate(f.readlines(), 1):
#         print(line)
        # result = split(line, STRING_LITERAL)
        # if len(result) > 1:
        #     print(f"{i}: {result[1]}")
#program, tokens, isOK = load_program("tests/string1.porth")    