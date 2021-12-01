#!/usr/bin/python3
# -*- coding: utf-8 -*-

from porth_globals import * 
from typing import *

error_counter = 0
macro_struct= {}

#returns the number of errors found
def get_counter_error() -> int:
    global error_counter
    return error_counter

#to manage list of comments types and not only one type of comment
def split(txt: str, seps:List) -> List:
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


# tokenize a file
def lex_file(filename: str) -> List[Dict]:
    with open(filename, "r") as f:
        return [{'loc': (filename, row, col), 'type': token_type, 'value': token } for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(filename, row, line)]


#separate a line into strings and non strings, calculate the start and end of each token and returns the list of tokens
#line here represents a subset(without comments) of the line
#probably to improve this part later
def separate_line(startline: int, line: str, sep: Literal) -> Tuple[List, List]:
    strings = []
    notstrings_temp = []
    notstrings = []
    start = 0
    nstart = 0
    nend = 0
    end = 0
    nb_quotes = 0
    for i in range(len(line)):
        if line[i] == sep:
            nb_quotes += 1
            #start new string or end new string
            if nb_quotes % 2 == 0:
                nstart = i + 1
                end = i 
                strings.append((startline + start, OP_STRING, line[start:end]))
            else:
                nend = i-1
                if nend < 0:
                    nend = 0
                notstrings_temp.extend(line[nstart:nend].split())
                #print(line[nstart:nend])
            start = i + 1
    notstrings_temp.extend(line[nstart:].split())
    notstrings.extend(parse_not_string(line, notstrings_temp))
    return strings, notstrings

#returns the list of tokens for non strings tokens, here line is the line of the original file
def parse_not_string(line: str, tokens: List) -> List[Tuple]:
    start = 0
    coltok= []
    for token in tokens:
        token_type = get_token_type(token)
        if token_type == OP_UNKNOWN:
            isMacro = check_if_macro_identifier(token)
            if isMacro:
                token_type = OP_IDMACRO
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token_type, token)) 
    return coltok

def reorganize_tokens(strings: List, notstrings: List) -> List:
    #print(strings, notstrings)
    organized_tokens = []
    temp_tokens = []
    #print(strings, notstrings)
    temp_tokens.extend(strings)
    temp_tokens.extend(notstrings)
    if len(temp_tokens) != 0:
        organized_tokens = sorted(temp_tokens, key=lambda tup: tup[0])
    #print(organized_tokens)
    return organized_tokens

#tokenize a line. Ignore comments. if double quotes try to parse strings and non strings tokens
#otherwise it assumes that each token is separate by a space
def lex_line(filename, row, line) -> List[Tuple]:
    global error_counter
    coltok= [] 
    strings= []
    linewithoutcomments = split(line, COMMENTS)
    startline= line.find(linewithoutcomments[0]) + 1
    if linewithoutcomments[0].count(DOUBLE_QUOTE) % 2 != 0:
        print(f"Error Code {ERR_TOK_STRING} Unbalanced quotes in line {row} ")
        error_counter += 1
        return coltok
    if OPMACRO in linewithoutcomments[0]:
        tokens = linewithoutcomments[0].split()
        #print(tokens)
        coltok.extend(parse_macro(filename, row, line, tokens))          
    elif DOUBLE_QUOTE in line:
        stringline = linewithoutcomments[0] 
        #print(stringline)
        strings, notstrings= separate_line(startline, stringline, DOUBLE_QUOTE)
        organized_tokens = reorganize_tokens(strings, notstrings)
        #print(strings, notstrings)
        coltok.extend(organized_tokens)
    else:
        tokens = linewithoutcomments[0].split()
        token_not_string = parse_not_string(line, tokens)
        coltok.extend(token_not_string)
    return coltok


#returns the list of forbidden tokens as first token in a line (probably need to be removed if we accept multilines for a single instruction)
def check_first_token(token: Any, forbidden_tokens: List) -> bool:
    isOK = False
    if token in forbidden_tokens:
        isOK = True
    return isOK


#returns the function corresponding to the token found
def parse_word(token: Dict) -> Dict:
    global error_counter
    filename, line, column = token['loc']
    word = token['value']
    tokentype = token['type']
    loc = (filename, line, column)
    if word in keyword_table:
        return {'type': keyword_table[word], 'loc': token['loc'], 'value': word, 'jmp': None}
    elif tokentype==OP_STRING:
        return {'type': tokentype, 'value': bytes(word, "utf-8").decode("unicode_escape"), 'loc': token['loc']}
    else:
        try :
            number = int(word)
            return {'type': OP_PUSH, 'loc': loc, 'value': number,  'jmp': None}                    
        except ValueError:
            # print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            # error_counter += 1
            # return {'type': OP_UNKNOWN, 'loc': (filename, line, column), 'value': word, 'jmp': None}
            isMacroId = check_if_macro_identifier(word)
            #print(isMacroId, word, loc)
            if not isMacroId:
                print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
                error_counter += 1
                return {'type': OP_UNKNOWN, 'loc': (filename, line, column), 'value': word, 'jmp': None}
            else:
                return {'type': OP_IDMACRO, 'loc': loc, 'value': word, 'jmp': None}


#returns the list of tokens for macro definition
def parse_macro(filename:str, row: int, line: str, tokens: List) -> List[Tuple]:
    global error_counter, macro_struct
    start = 0
    coltok= []
    if tokens[0] != OPMACRO:
        print(f"Error Code {ERR_TOK_MACRO} Macro keyword should be the first token in macro definition line {row}")
        error_counter += 1
    elif len(tokens) < 2:
        print(f"Error Code {ERR_TOK_MACRO} Macro definition should have 1 identifier following MACRO keyword error line {row}")
        error_counter += 1
    elif len(tokens) > 2:
        print(f"Error Code {ERR_TOK_MACRO} Macro definition inline macro not allowed for now only 1 identifier is allowed following MACRO keyword error line {row}")
        error_counter += 1        
    elif tokens[1] in keyword_table:
        print(f"Error Code {ERR_TOK_MACRO_ID} Macro identifier should not be a keyword! Keyword {tokens[1]} found as Macro Identifier at line {row}")
        error_counter += 1
    else:
        #check if macro already defined
        if tokens[1] in macro_struct:
            _, first_definition, _ = macro_struct[tokens[1]]['definition']
            print(f"Error Code {ERR_TOK_MACRO_ID} line {row} Macro identifier {tokens[1]} already defined at line {first_definition}")
            error_counter += 1
        else:
            macro_struct[tokens[1]] = {'args': None, 'definition': (filename, row, line[start:].find(tokens[1]))}
        #print(macro_struct)
        for token in tokens:
            token_type = get_token_type(token)
            loc = (filename, line, row)
            isMacroId = check_if_macro_identifier(token)
            if isMacroId:
                token_type = OP_IDMACRO
            col = line[start:].find(token) 
            start= col + start + 1  #adding 1 to start from column 1 instead of 0
            coltok.append((start, token_type, token)) 
    #print(macro_struct)
    return coltok

def check_if_macro_identifier(word: str) -> bool:
    global error_counter, macro_struct
    isMacroId = False
    #print(macro_struct)
    if word in macro_struct:
        isMacroId = True
    return isMacroId


#returns the program in the porth language after two passes : first tokenize and second calculate cross references for IF/END
def load_program(filename: str) -> Tuple[List, List, bool]:
    program, tokens, isOK = load_program_first_pass(filename)
    program_xref = program
    #program_expanded = program_xref
    if isOK:
        # program_xref, error = cross_reference_block(program)
        # if error:
        #     isOK = False
        # else:
        program_macro, error = pre_processing(program)
        if error:
            isOK = False
        else:        
            program_expanded = expand_macros(program_macro) 
            program_xref, error = cross_reference_block(program_expanded)
        #print(program_xref)
            if error:
                isOK = False
        #program_expanded = program_xref
    return program_xref, tokens, isOK


#do a first pass  to parse tokens and check for errors
def load_program_first_pass(filename: str) -> Tuple[List, List, bool]:
    global error_counter
    isOK = True
    tokens_output = []
    tokens = lex_file(filename)
    if error_counter > 0:
        isOK = False
        print(f"Error found during parsing ! {error_counter}")
    for i, token in enumerate(tokens):
        if (token['type'] == OP_INCLUDE and tokens[i+1]['type'] == OP_STRING) or (token['type'] == OP_STRING and tokens[i-1]['type'] == OP_INCLUDE):
            #print(token, tokens[i+1], tokens[i-1])
            if token['type'] == OP_STRING:
                try:
                    included_tokens=lex_file(tokens[i]['value'])
                    tokens_output.extend(included_tokens)
                    #print(included_tokens)
                except FileNotFoundError:
                    print(f"Error Code {ERR_TOK_INCLUDE} File {tokens[i]['value']} not found")
                    error_counter += 1
                    isOK = False
        else:
            tokens_output.append(token)
    if  any(d['value'] == OPINCLUDE for d in tokens_output):
        print(f"Error Code {ERR_TOK_INCLUDE} recursive include not implemented!")
        error_counter += 1
        isOK = False
        
    #print(tokens_output)
    # current_line = 0
    # first_token = False
    # for token in tokens:
    #     filename, line, col = token['loc']
    #     toktype = token['type']
    #     tok = token['value']
    #     if line != current_line:
    #         first_token = True            
    #         current_line = line
    #     if check_first_token(tok, forbidden_tokens) and first_token:
    #         print(f"Error Code {ERR_TOK_FORBIDDEN} Token {tok} is forbidden in first position in file {filename}, line {line} column {col}, type token {get_token_type(toktype)}")
    #         error_counter += 1
    #         first_token = False
    #         isOK = False
    #     first_token = False    
    return [parse_word(word) for word in tokens_output], tokens_output, isOK

#expand recursively all macros in the program
def expand_macros(program, recursive=False):
    global macro_struct
    #print(macro_struct)
    program_output = []
    omit = False
    for line in program:
        if line['type']== OP_MACRO:
            omit = True
        elif line['type']== OP_ENDM:
            omit = False
        else:
            if omit == False:
                if line['value'] in macro_struct:
                    if 'body' in macro_struct[line['value']]:
                        macro_body = macro_struct[line['value']]['body']
                        for body in macro_body:
                            program_output.append(body)
                            if body['value'] in macro_struct:
                                recursive = True
                else:
                    program_output.append(line)
    if recursive:
        program_output = expand_macros(program_output)
    return program_output

#fills the body of the macro 
def pre_processing(program: List) -> Tuple[List, bool]:
    global error_counter, macro_struct
    error_preproc = 0
    error = False
    nbmacros = 0
    macro_name = ""
    macro_body= []
    startingMacro= False   
    for ip in range(len(program)):
        filename, line, col = program[ip]['loc']
        op = program[ip]
        if op['type'] == OP_MACRO:
            nbmacros += 1
            startingMacro = True
            macro_name= program[ip + 1]['value']
            macro_body= []
        elif op['type'] == OP_ENDM:
            if startingMacro==True:
                startingMacro= False
                nbmacros -= 1
                if macro_name in macro_struct:
                    if 'body' not in macro_struct[macro_name]:
                        _ , macro_def_line, _ = macro_struct[macro_name]['definition']
                        print(f"Error Code {ERR_MACRO_EMPTY} empty body macro in file {filename} between line {macro_def_line} line {line}")
                        error_preproc += 1
            else:
                print(f"Error Code {ERR_TOK_BLOCK} ENDM without MACRO in file {filename}, line {line} column {col}")
                error_preproc += 1                 
        #to allow macros in the body of other macros
        elif startingMacro==True and program[ip - 1 ]['type'] != OP_MACRO:
            macro_body.append(op)
            if macro_name in macro_struct:
                macro_struct[macro_name]['body'] = macro_body
    if nbmacros != 0:
        print(f"Error Code {ERR_MACRO_ENDM} ENDM missing one")
        error_preproc += 1 
    if error_preproc > 0:
        print(f"{error_preproc} errors found during pre-processing")  
        error_counter = error_counter + error_preproc      
        error= True             
    return program, error


#cross references to store the link between a IF and this corresponding END operation!
def cross_reference_block(program: List) -> Tuple[List, bool]:
    global error_counter, macro_struct
    error_xrefs = 0
    stack = []
    ifarray= []
    error = False
    for ip in range(len(program)):
        filename, line, col, *_ = program[ip]['loc']
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

