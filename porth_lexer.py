#!/usr/bin/python3
# -*- coding: utf-8 -*-

from porth_globals import * 
from typing import *
from porth_error import generate_error, check_errors

#to manage list of comments types and not only one type of comment
def split(txt: str, seps:List) -> List:
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


# tokenize a file
def lex_file(filename: str) -> Tuple[List[Dict], bool]:
    global error_counter, error_msg
    errfunction = 'lex_file'
    isOK = True
    try:
        with open(filename, "r") as f:
            return [{'loc': (filename, row, col), 'type': token_type, 'value': token } for (row, line) in enumerate(f.readlines(), 1) for (col, token_type, token) in lex_line(filename, row, line)], isOK
    except FileNotFoundError:
        #print(f"Error Code {ERR_TOK_FILE} File {filename} not found")
        generate_error(filename=filename, errfunction=errfunction, msgid= 0)
        isOK= False
        return [], isOK


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
    for i, token in enumerate(tokens):
        token_type = get_token_type(token)
        if token_type == OP_UNKNOWN:
            if check_if_macro_identifier(token):
                token_type = OP_IDMACRO
            elif check_if_var_identifier(token):
                token_type = OP_IDVAR
            else: 
                #print(tokens)
                #manage specific case of ' '
                if tokens[i] == SINGLE_QUOTE and tokens[i+1]== SINGLE_QUOTE:
                    token_type = OP_CHAR
                    token = tokens[i] +  " " + tokens[i+1]
                    col = line[start:].find(token)
                    coltok.append((start, token_type, token)) 
                    continue
                elif tokens[i] ==SINGLE_QUOTE and tokens[i-1]== SINGLE_QUOTE:
                    continue
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token_type, token)) 
    return coltok

def reorganize_tokens(strings: List, notstrings: List) -> List:
    organized_tokens = []
    temp_tokens = []
    temp_tokens.extend(strings)
    temp_tokens.extend(notstrings)
    if len(temp_tokens) != 0:
        organized_tokens = sorted(temp_tokens, key=lambda tup: tup[0])
    return organized_tokens

#tokenize a line. Ignore comments. if double quotes try to parse strings and non strings tokens
#otherwise it assumes that each token is separate by a space
def lex_line(filename, row, line) -> List[Tuple]:
    global error_counter
    coltok= [] 
    line_to_parse = split(line, COMMENTS)[0]
    tokens = line_to_parse.split()
    startline= line.find(line_to_parse) + 1
    if OPMACRO in line_to_parse:
        coltok.extend(parse_macro(filename, row, line, tokens))          
    elif DOUBLE_QUOTE in line:  
        strings, notstrings= separate_line(startline, line_to_parse, DOUBLE_QUOTE)
        organized_tokens = reorganize_tokens(strings, notstrings)
        coltok.extend(organized_tokens)
    else:
        if OPVAR in line_to_parse:
            coltok.extend(parse_var(filename, row, line, tokens))
        else:
            token_not_string = parse_not_string(line, tokens)
            coltok.extend(token_not_string)
    return coltok

#check if the token is a variable identifier
def parse_var(filename:str, row: int, line: str, tokens: List) -> Dict:
    global var_struct, error_counter, error_msg
    errfunction = 'parse_var'
    start = 0
    coltok= []
    if tokens[0] != OPVAR:
        #print(f"Error Code {ERR_TOK_VAR} VAR keyword should be the first token in variable definition line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 1, fromline=row)
    elif len(tokens) < 3:
        #print(f"Error Code {ERR_TOK_VAR_DEF} Variable definition should be like VAR x u8  (x variable name and u8 variable type) error line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 2, fromline=row)
    elif len(tokens) > 5:
        #print(f"Error Code {ERR_TOK_VAR_DEF} Variable definition should be like VAR x u8 100 !x (x variable name and u8 variable type value and assignment operator) error line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 3, fromline=row)      
    elif tokens[1] in keyword_table:
        #print(f"Error Code {ERR_TOK_VAR_ID} Variable identifier should not be a keyword! Keyword {tokens[1]} found as Variable Identifier at line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 4, token=tokens[1], fromline=row)      
    elif tokens[2] not in VAR_TYPE:
        #print(f"Error Code {ERR_TOK_VAR_TYPE} Variable type should be one of {VAR_TYPE} error line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 5, fromline=row)          
    else:
        #check if variable already defined
        if tokens[1] in var_struct:
            _, first_definition, _ = var_struct[tokens[1]]['definition']
            #print(f"Error Code {ERR_TOK_VAR_ID} line {row} VAR identifier {tokens[1]} already defined at line {first_definition}")
            generate_error(filename=filename, errfunction=errfunction, msgid= 6, fromline=row)              
        elif tokens[1] in macro_struct:
            _, first_definition, _ = macro_struct[tokens[1]]['definition']
            #print(f"Error Code {ERR_TOK_VAR_ID} line {row} VAR identifier {tokens[1]} already defined as macro at line {first_definition}")
            generate_error(filename=filename, errfunction=errfunction, msgid= 7, token=tokens[1], fromline=first_definition)              
        elif tokens[1] in reserved_words:
            #print(f"Error Code {ERR_TOK_VAR_ID} line {row} VAR identifier {tokens[1]} is a reserved word")
            generate_error(filename=filename, errfunction=errfunction, msgid= 16, token=tokens[1], fromline=row)
        else:
            if len(tokens) > 3:
                var_struct[tokens[1]] = {'definition': (filename, row, line[start:].find(tokens[1])), 'type': tokens[2], 'value': tokens[3], 'used': 0}
            else:
                var_struct[tokens[1]] = {'definition': (filename, row, line[start:].find(tokens[1])), 'type': tokens[2], 'value': None, 'used': 0}
        for token in tokens:
            token_type = get_token_type(token)
            if check_if_var_identifier(token):
                token_type = OP_IDVAR
            elif token in VAR_TYPE:
                token_type = OP_VARTYPE
            elif check_if_var_assign_operator(token):
                token_type = OP_ASSIGN_VAR
            col = line[start:].find(token) 
            start= col + start + 1  #adding 1 to start from column 1 instead of 0
            coltok.append((start, token_type, token)) 
    return coltok

#returns the function corresponding to the token found
def parse_word(token: Dict) -> Dict:
    global error_counter
    errfunction = 'parse_word'    
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
            if check_if_char(word)==True:
                #managing special characters see in porth_globals the exhaustive list
                if len(word)==4:
                    if word[1:3] in special_chars:
                        #char_int = ord(special_chars[word[1:3]].encode("utf-8"))
                        char_int = ord(special_chars[word[1:3]])
                else:
                    #char_int = ord(word[1].encode('utf-8'))
                    char_int = ord(word[1])
                return {'type': OP_CHAR, 'loc': loc, 'value': char_int, 'jmp': None}
            elif check_if_macro_identifier(word)==True:
                return {'type': OP_IDMACRO, 'loc': loc, 'value': word, 'jmp': None}
            elif check_if_var_identifier(word)==True:
                return {'type': OP_IDVAR, 'loc': loc, 'value': word, 'jmp': None}
            elif check_if_var_type(word)==True:
                return {'type': OP_VARTYPE, 'loc': loc, 'value': word, 'jmp': None}
            elif check_if_var_assign_operator(word) ==True:
                return {'type': OP_ASSIGN_VAR, 'loc': loc, 'value': word, 'jmp': None, 'variable': word[1:]}
            elif word in reserved_words:
                return {'type': OP_UNKNOWN, 'loc': (filename, line, column), 'value': word, 'jmp': None}
            else:
                #print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 8, token=word, fromline=line, column=column)                  
                return {'type': OP_UNKNOWN, 'loc': (filename, line, column), 'value': word, 'jmp': None}


#returns the list of tokens for macro definition
def parse_macro(filename:str, row: int, line: str, tokens: List) -> List[Tuple]:
    global error_counter, macro_struct
    errfunction = 'parse_macro'
    start = 0
    coltok= []
    if tokens[0] != OPMACRO:
        #print(f"Error Code {ERR_TOK_MACRO} Macro keyword should be the first token in macro definition line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 9, fromline=row)           
    elif len(tokens) < 2:
        #print(f"Error Code {ERR_TOK_MACRO} Macro definition should have 1 identifier following MACRO keyword error line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 10, fromline=row)              
    elif tokens[1] in keyword_table:
        #print(f"Error Code {ERR_TOK_MACRO_ID} Macro identifier should not be a keyword! Keyword {tokens[1]} found as Macro Identifier at line {row}")
        generate_error(filename=filename, errfunction=errfunction, msgid= 11, token=tokens[1], fromline=row)              
    elif tokens[1] in var_struct:
            _, first_definition, _ = var_struct[tokens[1]]['definition']
            #print(f"Error Code {ERR_TOK_VAR_ID} line {row} MACRO identifier {tokens[1]} already defined as variable at line {first_definition}")
            generate_error(filename=filename, errfunction=errfunction, msgid= 12, token=tokens[1], fromline=first_definition)              
    else:
        #check if macro already defined
        if tokens[1] in macro_struct:
            _, first_definition, _ = macro_struct[tokens[1]]['definition']
            #print(f"Error Code {ERR_TOK_MACRO_ID} line {row} Macro identifier {tokens[1]} already defined at line {first_definition}")
            generate_error(filename=filename, errfunction=errfunction, msgid= 13, token=tokens[1], fromline=row, toline=first_definition)                          
        elif tokens[1] in reserved_words:
            #print(f"Error Code {ERR_TOK_MACRO_ID} line {row} Macro identifier {tokens[1]} is a reserved word")
            generate_error(filename=filename, errfunction=errfunction, msgid= 29, token=tokens[1], fromline=row)
        else:
            macro_struct[tokens[1]] = {'args': None, 'definition': (filename, row, line[start:].find(tokens[1]))}
        for token in tokens:
            token_type = get_token_type(token)
            #loc = (filename, line, row)
            isMacroId = check_if_macro_identifier(token)
            if isMacroId:
                token_type = OP_IDMACRO
            col = line[start:].find(token) 
            start= col + start + 1  #adding 1 to start from column 1 instead of 0
            coltok.append((start, token_type, token)) 
    return coltok

#returns True if the token is a variable type
def check_if_var_type(word: str) -> bool:
    global VAR_TYPE
    isVarType = False
    if word in VAR_TYPE:
        isVarType = True
    return isVarType

#returns True if the token is a assingment variable operation
def check_if_var_assign_operator(word: str) -> bool:
    isVarAssignOp = False
    if len(word) > 1 and word[0] == OPASSIGN and word[1:] in var_struct:
        isVarAssignOp = True
    return isVarAssignOp

#returns True if the token is a variable identifier
def check_if_var_identifier(word: str) -> bool:
    global var_struct
    isVarId = False
    if word in var_struct:
        isVarId = True
    return isVarId

#returns True if the token is a macro identifier
def check_if_macro_identifier(word: str) -> bool:
    isMacroId = False
    if word in macro_struct:
        isMacroId = True
    return isMacroId

#returns True if the token is a char. A char should have for now a single character between single quotes
def check_if_char(word: str) -> bool:
    isAChar = False
    if word.startswith("'") and word.endswith("'") and len(word) == 3:
        isAChar = True
    elif word.startswith("'") and word.endswith("'") and len(word) == 4:
        if word[1] == '\\':
            isAChar = True
    return isAChar


#returns the program in the porth language after two passes : first tokenize and second calculate cross references for IF/END
def load_program(filename: str) -> Tuple[List, List, bool]:
    global error_counter
    errfunction = 'load_program'
    isOK = True
    #manage includes
    program, tokens, isOK = pre_processing_includes(filename)
    if check_errors():
        isOK = False
    program_xref = program
    #program_expanded = program_xref
    if isOK:
        #manage macros
        program_macro, error = pre_processing_macros(program)
        if error:
            isOK = False
        else:        
            program_expanded = expand_macros(program_macro) 
            #manage cross references for blocks
            program_xref, error = cross_reference_block(program_expanded)
            if error:
                isOK = False
    return program_xref, tokens, isOK


def recursive_includes(filename: str, tokens_temp: List ) -> List:
    global error_counter, include_file
    errfunction = 'recursive_includes'
    tokens_output = []
    isOK = True
    for i, token in enumerate(tokens_temp):
        if (token['type'] == OP_INCLUDE and tokens_temp[i+1]['type'] == OP_STRING) or (token['type'] == OP_STRING and tokens_temp[i-1]['type'] == OP_INCLUDE):
            if token['type'] == OP_STRING:
                try:
                    if tokens_temp[i]['value'] not in include_file:
                        included_tokens, isOK=lex_file(tokens_temp[i]['value'])
                        include_file.append(tokens_temp[i]['value'])
                        tokens_output.extend(included_tokens)
                except FileNotFoundError:
                    #print(f"Error Code {ERR_TOK_INCLUDE} File {tokens_temp[i]['value']} not found")
                    generate_error(filename=filename, errfunction=errfunction, msgid= 15, token=tokens_temp[i]['value'])                          
                    isOK = False
        else:
            tokens_output.append(token)
    return tokens_output, isOK


#do a first pass  to parse tokens and check for errors
def pre_processing_includes(filename: str, recursive: bool = False) -> Tuple[List, List, bool]:
    global error_counter, include_file
    errfunction = 'pre_processing_includes'
    tokens_output = []
    isOK = True
    tokens, isOK = lex_file(filename)
    if isOK==False:
        return [], [], isOK
    tokens_output, isOK  = recursive_includes(filename, tokens)
    #managing recursive includes
    while isOK and any(d['value'] == OPINCLUDE for d in tokens_output):
        tokens_temp = tokens_output
        tokens_output, isOK = recursive_includes(filename, tokens_temp)
    return [parse_word(word) for word in tokens_output], tokens_output, isOK

#expand recursively all macros in the program
def expand_macros(program, recursive=False):
    global macro_struct
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
def pre_processing_macros(program: List) -> Tuple[List, bool]:
    global error_counter, macro_struct
    errfunction = 'pre_processing_macros'
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
                        #print(f"Error Code {ERR_MACRO_EMPTY} empty body macro in file {filename} between line {macro_def_line} line {line}")
                        generate_error(filename=filename, errfunction=errfunction, msgid= 17, token=macro_name, fromline=macro_def_line, toline=line) 
            else:
                #print(f"Error Code {ERR_TOK_BLOCK} ENDM without MACRO in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 18, fromline=line, column=col) 
        #to allow macros in the body of other macros
        elif startingMacro==True and program[ip - 1 ]['type'] != OP_MACRO:
            macro_body.append(op)
            if macro_name in macro_struct:
                macro_struct[macro_name]['body'] = macro_body
    if nbmacros != 0:
        #print(f"Error Code {ERR_MACRO_ENDM} ENDM missing one")
        generate_error(filename=filename, errfunction=errfunction, msgid= 19) 
    #detecting recursive macro. 
    for macro in macro_struct:
        if 'body' in macro_struct[macro]:
            macro_index = next((index for (index, d) in enumerate(macro_struct[macro]['body']) if d["value"] == macro), None)
            if macro_index != None:
                _ , line_recursive, _ = macro_struct[macro]['body'][macro_index]['loc']
                #print(f"Error Code {ERR_MACRO_RECURSIVE} macro `{macro}` recursive definition in file {filename} line {line_recursive}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 20, token=macro, fromline=line_recursive) 
    if check_errors():
        error= True             
    return program, error


#cross references to store the link between a IF and this corresponding END operation!
def cross_reference_block(program: List) -> Tuple[List, bool]:
    global error_counter, macro_struct, var_struct, error_msg, files_struct
    errfunction = 'cross_reference_block'
    stack = []
    ifarray= []
    error = False
    level = 0
    var_used = 0
    index_file = 3
    for ip in range(len(program)):
        filename, line, col, *_ = program[ip]['loc']
        op = program[ip]
        if op['type'] == OP_IF:
            stack.append(ip)
            ifarray.append(ip)
        elif op['type'] == OP_ELSE:    
            if len(ifarray) == 0:
                #print(f"Error Code {ERR_TOK_BLOCK} ELSE without IF in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 21, fromline=line, column=col) 
            else:
                if_ip = stack.pop()
                program[if_ip]['jmp'] = ip + 1
                stack.append(ip)  
        elif op['type'] == OP_END:
            if len(ifarray) == 0 :
                #print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 22, fromline=line, column=col) 
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
                    #print(f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {line} column {col}, in file {filename}")
                    generate_error(filename=filename, errfunction=errfunction, msgid= 22, fromline=line, column=col)                     
        elif op['type'] == OP_WHILE:
            stack.append(ip)
        elif op['type'] == OP_DO:
            ifarray.append(ip)
            if len(stack) == 0:
                #print(f"Error Code {ERR_TOK_BLOCK} DO without WHILE in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 23, fromline=line, column=col)                 
            else:
                while_ip = stack.pop()
                program[ip]['jmp'] = while_ip
                stack.append(ip)
                program[ip]['level'] = level
                level += 1
        elif op['type'] == OP_IDVAR:
            def_line = var_struct[op['value']]['definition'][1]
            current_line = op['loc'][1]
            if current_line < def_line:
                #print(f"Error Code {ERR_VAR_UNDEF} variable `{op['value']}` used before definition in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 24, token=op['value'], fromline=line, column=col) 
            #store the number of a variable is used    
            elif current_line != def_line:
                var_used = var_struct[op['value']]['used']
                var_used += 1
                var_struct[op['value']]['used'] = var_used
        elif op['type'] == OP_ASSIGN_VAR:
            var =  op['value'][1:]            
            def_line = var_struct[var]['definition'][1] 
            current_line = op['loc'][1]       
            if program[ip - 1]['type'] in (OP_OPEN, OP_CLOSE, OP_OPENW, OP_READF, OP_WRITEF):
                op['index'] = program[ip - 1]['index']
                var_struct[var]['value'] =  program[ip - 1]['index']   
                #print(var_struct,  program[ip - 1]['value'])
            if current_line < def_line:
                #print(f"Error Code {ERR_VAR_UNDEF} variable `{op['value']}` used before definition in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 24, token=op['value'], fromline=line, column=col) 
            #store the number of a variable is used    
            elif program[ip - 1]['type'] == OP_DIVMOD:
                #print(f"Error Code {ERR_VAR_NOT_ALW} variable `{op['value']}` can't be used after DIVMOD operator. Error in file {filename}, line {line} column {col}")
                generate_error(filename=filename, errfunction=errfunction, msgid= 14, token=op['value'], fromline=line, column=col)
            elif current_line != def_line:
                #print(program[ip])
                var_used = var_struct[var]['used']
                var_used += 1
                var_struct[var]['used'] = var_used
        elif op['type'] == OP_VARTYPE:
            if ip <= 1:
                generate_error(filename=filename, errfunction=errfunction, msgid= 27, fromline=line, column=col)                 
            elif  program[ip - 1]['type'] != OP_IDVAR or program[ip - 2]['type'] != OP_VAR:
                generate_error(filename=filename, errfunction=errfunction, msgid= 27, fromline=line, column=col)                 
        # open file and store it in the files_struct
        elif op['type'] == OP_OPEN:
            files_struct[index_file] = {"filename": program[ip - 1]['value'], "close": False, "index": index_file, "options": 0}
            op['index'] = index_file
            op['options'] = 0
            index_file += 1

        # open file for writing mode and store it in the files_struct            
        elif op['type'] == OP_OPENW:
            files_struct[index_file] = {"filename": program[ip - 1]['value'], "close": False, "index": index_file, "options": 1}
            op['index'] = index_file
            op['options'] = O_CREAT|O_WRONLY|O_TRUNC
            index_file += 1 
        # close or readf or writef : update file index in the op code
        elif op['type'] == OP_CLOSE or op['type'] == OP_READF or op['type'] == OP_WRITEF:
            if program[ip - 1]['value'] in var_struct:
                #print(var_struct[program[ip - 1]['value']])
                op['index'] = var_struct[program[ip - 1]['value']]['value']
            else:
                op['index'] = program[ip - 1]['value']
    if len(ifarray) > 0:
        #print(f"Error Code {ERR_TOK_BLOCK} DO IF ELSE END missing one")
        generate_error(filename=filename, errfunction=errfunction, msgid= 28) 
    if check_errors():
        error= True
    return program, error


