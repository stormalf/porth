#!/usr/bin/pypy3
# -*- coding: utf-8 -*-

from porth_globals import * 
from typing import *

error_table = {}
warning_table = {}
runtime_table = {}

#returns the number of errors found
def get_counter_error() -> int:
    global error_counter
    return error_counter

#returns the number of warnings found
def get_counter_warning() -> int:
    global warning_counter
    return warning_counter    

runtime_error_counter = 0

def get_runtime_error() -> int:
    global runtime_error_counter
    return runtime_error_counter


def set_runtime_error() -> int:
    global runtime_error_counter
    runtime_error_counter += 1


def generate_error(filename:str, errfunction: str, msgid: int, fromline: int = 0, column: int = 0, token: str = None, toline: int = 0, increment=True) -> str:
    global error_counter, error_msg
    error_msg[error_counter]= {'msg': error_management(filename=filename, msgid= msgid, fromline=fromline, column=column, token=token, toline=toline), 'function': errfunction}
    if increment:
        error_counter += 1
    #return error_management(filename, msgid, fromline, column, token, toline)


def error_management(filename:str, msgid: int, fromline: int = 0, column: int = 0, token: str = None, toline: int = 0) -> str:
    global error_table, error_counter, error_xrefs
    error_table[0] = f"Error Code {ERR_TOK_FILE} File {filename} not found"
    error_table[1] = f"Error Code {ERR_TOK_VAR} VAR keyword should be the first token in variable definition line {column}"
    error_table[2] = f"Error Code {ERR_TOK_VAR_DEF} Variable definition should be like VAR x u8  (x variable name and u8 variable type) error line {column}"
    error_table[3] = f"Error Code {ERR_TOK_VAR_DEF} Variable definition should be like VAR x u8 100 !x (x variable name and u8 variable type value and assignment operator concatenate with th variable) error line {column}"
    error_table[4] = f"Error Code {ERR_TOK_VAR_ID} Variable identifier should not be a keyword! Keyword {token} found as Variable Identifier at line {column}"
    error_table[5] = f"Error Code {ERR_TOK_VAR_TYPE} Variable type should be one of {VAR_TYPE} error line {column}"
    error_table[6] = f"Error Code {ERR_TOK_VAR_ID} line {column} VAR identifier {token} already defined at line {fromline}"
    error_table[7] = f"Error Code {ERR_TOK_VAR_ID} line {column} VAR identifier {token} already defined as macro at line {fromline}"
    error_table[8] = f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {token} at line {fromline}, column {column} in file {filename}"
    error_table[9] = f"Error Code {ERR_TOK_MACRO} Macro keyword should be the first token in macro definition line {column}"
    error_table[10] = f"Error Code {ERR_TOK_MACRO} Macro definition should have 1 identifier following MACRO keyword error line {column}"
    error_table[11] = f"Error Code {ERR_TOK_MACRO_ID} Macro identifier should not be a keyword! Keyword {token} found as Macro Identifier at line {column}"
    error_table[12] = f"Error Code {ERR_TOK_VAR_ID} line {column} MACRO identifier {token} already defined as variable at line {fromline}"
    error_table[13] = f"Error Code {ERR_TOK_MACRO_ID} line {column} Macro identifier {token} already defined at line {fromline}"
    error_table[14] = f"Error Code {ERR_VAR_NOT_ALW} assignment variable `{token}` can't be used after DIVMOD operator. Error in file {filename}, line {fromline} column {column}"
    error_table[15] = f"Error Code {ERR_TOK_INCLUDE} File {token} not found"
    error_table[16] = f"Error Code {ERR_TOK_VAR_ID} line {column} VAR identifier {token} is a reserved word"
    error_table[17] = f"Error Code {ERR_MACRO_EMPTY} empty body macro {token} in file {filename} between line {fromline} line {toline}"
    error_table[18] = f"Error Code {ERR_TOK_BLOCK} ENDM without MACRO in file {filename}, line {fromline} column {column}"
    error_table[19] = f"Error Code {ERR_MACRO_ENDM} ENDM missing one"
    error_table[20] = f"Error Code {ERR_MACRO_RECURSIVE} macro `{token}` recursive definition in file {filename} line {fromline}"
    error_table[21] = f"Error Code {ERR_TOK_BLOCK} ELSE without IF in file {filename}, line {fromline} column {column}"
    error_table[22] = f"Error Code {ERR_TOK_BLOCK} END without IF/ELSE/DO at line {fromline} column {column}, in file {filename}"
    error_table[23] = f"Error Code {ERR_TOK_BLOCK} DO without WHILE in file {filename}, line {fromline} column {column}"
    error_table[24] = f"Error Code {ERR_VAR_UNDEF} variable `{token}` used before definition in file {filename}, line {fromline} column {column}"
    error_table[25] = f"Error Code {ERR_VAR_ASSIGN} trying to use ! operator without enough values in file {filename}, line {fromline} column {column}"
    error_table[26] = f"Error code {ERR_VAR_ASSIGN} impossible to assign something to a non variable in file {filename}, line {fromline} column {column}"
    error_table[27] = f"Error Code {ERR_VAR_TYPE} Incorrect use of VAR_TYPE keyword in file {filename}, line {fromline} column {column}"
    error_table[28] = f"Error Code {ERR_TOK_BLOCK} DO IF ELSE END missing one"
    error_table[29] = f"Error Code {ERR_TOK_MACRO_ID} line {column} Macro identifier {token} is a reserved word at line {fromline}"
    error_table[30] = f"Error Code {ERR_VAR_ASSIGN} impossible to assign specified value for the variable type in file {filename}, line {fromline} column {column}"
    error_table[31] = f"Error Code {ERR_TOK_FILE} file {token} not closed in file {filename}"
    error_table[32] = f"Error Code {ERR_TOK_FILE} file already closed in file {filename}, line {fromline} column {column}"
    assert len(error_table) == get_MAX_ERROR(), "Max error table implemented!"      
    return error_table[msgid]

def warning_management(filename:str, msgid: int, fromline: int, column: int, token: str, toline: int = 0) -> str:
    global warning_counter, warning_table
    warning_table[0] = f"Warning Code {WARN_VAR_UNUSED} variable `{token}` is defined in line {fromline} but never used in file {filename}"
    warning_table[1] = f"Warning Code {WARN_STACK_NOTEMPTY} stack not empty at end of file {filename}"
    assert len(warning_table) == get_MAX_WARNING(), "Max warning table implemented!"      
    return warning_table[msgid]



#check if warning and fills a dictionary with warnings to print
def check_warnings(filename: str) -> bool:
    global warning_counter, warning_msg
    haveWarning = False
    for i, var in enumerate(var_struct):
        if var_struct[var]['used'] == 0:
            warning_msg[0] = f"Warning Code {WARN_VAR_UNUSED} variable `{var}` is defined in line {var_struct[var]['definition'][1]} but never used in file {filename}"
            warning_counter += 1
            haveWarning = True
    #by default stack is not empty it contains number of arguments argc (1 by default for program name) following by all variables defined in the program and not deleting at the end
    # not sure how to destroy the variables in the stack at the end probably need a kind of garbage collector ?           
    if get_stack_counter() != 0:
        warning_msg[1] = f"Warning Code {WARN_STACK_NOTEMPTY} stack not empty at end of file {filename}: {get_stack_counter()} values left on stack"
        warning_counter += 1
        haveWarning = True
        warning_counter += 1
        haveWarning = True
    return haveWarning

#check if warning and fills a dictionary with warnings to print
def print_warnings() -> None:
    global warning_msg
    for msg in warning_msg:
            print(warning_msg[msg])

def check_errors() -> bool:
    global error_counter
    haveError = False
    if error_counter > 0:
        haveError = True
    return haveError

def print_errors() -> None:
    global error_msg
    #print(error_msg)
    for msg in error_msg:
            print(f"{error_msg[msg]['msg']} in function {error_msg[msg]['function']}")

def check_runtime_errors() -> bool:
    haveError = False
    if get_runtime_error() > 0:
        haveError = True
    return haveError

def print_runtime_errors() -> None:
    global runtime_msg
    for msg in runtime_msg:
        print(f"{runtime_msg[msg]['msg']} in function {runtime_msg[msg]['function']}")
            


def generate_runtime_error(op: Dict,  errfunction: str, msgid: int, toline: int = 0, increment=True) -> str:
    global runtime_error_counter, runtime_msg
    filename, fromline, column = op['loc']
    token = op['value']
    runtime_msg[runtime_error_counter]= {'msg': runtime_error_management(filename=filename, msgid= msgid, fromline=fromline, column=column, token=token, toline=toline), 'function': errfunction}
    if increment:
        set_runtime_error()


def runtime_error_management(filename:str, msgid: int, fromline: int = 0, column: int = 0, token: str = None, toline: int = 0) -> str:
    global runtime_table
    runtime_table[0] = f"Runtime Error Code {RUN_STK_ERR} in file {filename} line {fromline} column {column} `{token}` impossible not enough element in stack"
    runtime_table[1] = f"Runtime Error Code {RUN_JMP_ERR} in file {filename} line {fromline} column {column} `{token}` statement without jmp"
    runtime_table[2] = f"Runtime Error Code {RUN_INFINITE_LOOP} in file {filename} line {fromline} column {column} `{token}` infinite loop detected!"
    runtime_table[3] = f"Runtime Error Code {RUN_DIV_ZERO} in file {filename} line {fromline} column {column} `{token}` division by zero!"
    runtime_table[4] = f"Runtime Error Code {RUN_SYSCALL_ERR} in file {filename} line {fromline} column {column} `{token}`  unknown system call!"
    runtime_table[5] = f"Runtime Error Code {RUN_NOTYET_ERR} in file {filename} line {fromline} column {column} `{token}`  not yet implemented!"
    runtime_table[6] = f"Runtime Error Code {RUN_MEM_ERR} in file {filename} line {fromline} column {column} `{token}`  arg2 cannot be 0!"
    runtime_table[7] = f"Runtime Error Code {RUN_FILE_ERR} in file {filename} line {fromline} column {column} `{token}`  unknown file descriptor!"
    runtime_table[8] = f"Runtime Error Code {RUN_VAR_ERR} in file {filename} line {fromline} column {column} `{token}`  invalid value for the variable type!"
    return runtime_table[msgid]

#print(error_management("test", 3, 1, 1, "VAR"))