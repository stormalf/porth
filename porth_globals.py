#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import *

#Need to increase the max_ops each time we add a new opcode
MAX_OPS = 52

#max memory size
MEM_CAPACITY = 640_000
STR_CAPACITY = 640_000
#VAR_CAPACITY = 640_000

MAX_LOOP_SECURITY = 10_000_000

exit_code = 0
var_struct = {}


#list of comments types probably I'll prefer the python comment syntax for myself
#I keep only two // and # I removed the ; perhaps we need it later for other operation code
#COMMENTS = ["//", "#", ";"]
COMMENTS = ["//", "#"]

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
#STRING_LITERAL = [DOUBLE_QUOTE, " "]


iota_counter= 0


#enum function in python 
def iota(reset=False) -> int:
    global iota_counter
    if reset:
        iota_counter=0
    else:
        iota_counter+=1
    return iota_counter

def get_var_value(var: Union[str, int]) -> int:
    global var_struct
    if var in var_struct:
        return var_struct[var]['value']
    else:
        return var
    
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
OP_GE=iota()
OP_LE=iota()
OP_NE=iota()
OP_DIV=iota()
OP_MUL=iota()
OP_DIVMOD=iota()
OP_WHILE=iota()
OP_DO=iota()
OP_MEM=iota()
OP_LOAD=iota()
OP_STORE=iota()
OP_SYSCALL0=iota()
OP_SYSCALL1=iota()
OP_SYSCALL2=iota()
OP_SYSCALL3=iota()
OP_SYSCALL4=iota()
OP_SYSCALL5=iota()
OP_SYSCALL6=iota()
OP_DUP2=iota()
OP_EXIT=iota()
OP_WRITE=iota()
OP_SWAP=iota()
OP_DROP=iota()
OP_SHL=iota()
OP_SHR=iota()
OP_ORB=iota()
OP_ANDB=iota()
OP_OVER=iota()
OP_MOD=iota()
OP_STRING=iota()
OP_MACRO=iota()
OP_IDMACRO=iota()
OP_ENDM=iota()
OP_INCLUDE=iota()
OP_CHAR=iota()
OP_VAR=iota()
OP_ASSIGN=iota()
OP_IDVAR=iota()
OP_VARTYPE=iota()
#keep in last line to have the counter working
COUNT_OPS=iota()

#error code parsing
ERR_TOK_NOERROR=iota(True)
ERR_TOK_UNKNOWN=iota()
#ERR_TOK_FORBIDDEN=iota()
ERR_TOK_BLOCK=iota()
ERR_TOK_STRING=iota()
ERR_TOK_MACRO=iota()
ERR_TOK_MACRO_ID=iota()
ERR_MACRO_EMPTY=iota()
ERR_MACRO_ENDM=iota()
ERR_MACRO_RECURSIVE=iota()
ERR_TOK_INCLUDE=iota()
ERR_TOK_FILE=iota()
ERR_TOK_VAR=iota()
ERR_TOK_VAR_DEF=iota()
ERR_TOK_VAR_ID=iota()
ERR_TOK_VAR_TYPE=iota()

#error codes runtime
RUN_NO_ERROR=iota(True)
RUN_DIV_ZERO=iota()
RUN_UNKNOWN=iota()
RUN_INFINITE_LOOP=iota()

RUNTIME_ERROR = {
    RUN_DIV_ZERO: "Division by zero!",
    RUN_UNKNOWN: "Unknown error!",
    RUN_INFINITE_LOOP: "Infinite loop!"
} 


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
STRING= "string"
CHAR="char"
OPDUP="DUP"
OPDUP2="2DUP"
OPGT = ">"
OPLT = "<"
OPGE=">="
OPLE="<="
OPNE="!="
OPDIV= "DIV"
OPDIVMOD="DIVMOD"
OPMUL="MUL"
OPWHILE = "WHILE"
OPDO = "DO"
OPMEM = "MEM"
OPLOAD= "$"
OPSTORE="@"
OPSYSCALL0= "SYSCALL0"
OPSYSCALL1="SYSCALL1"
OPSYSCALL2="SYSCALL2"
OPSYSCALL3="SYSCALL3"
OPSYSCALL4="SYSCALL4"
OPSYSCALL5="SYSCALL5"
OPSYSCALL6="SYSCALL6"
OPEXIT="EXIT"
OPWRITE="WRITE"
OPSWAP="SWAP"
OPDROP="DROP"
OPSHL="SHL"
OPSHR="SHR"
OPORB= "ORB"
OPANDB="ANDB"
OPOVER="OVER"
OPMOD="MOD"
OPMACRO="MACRO"
OPIDMACRO="idmacro"
OPENDM="ENDM"
OPINCLUDE="INCLUDE"
OPVAR="VAR"
OPASSIGN="!"
OPIDVAR="idvar"
OPU8="u8"
OPU16="u16"
OPU32="u32"
OPU64="u64"
# OPI8="i8"
# OPI16="i16"
# OPI32="i32"
# OPI64="i64"
# OPF32="f32"
# OPF64="f64"
# OPSTRING="str"
# OPCHAR="char"

VAR_TYPE=[OPU8,OPU16,OPU32,OPU64]

#forbidden_tokens = [PLUS, MINUS, DUMP]

def get_MAX_OPS() -> int:
    return MAX_OPS    

def get_MEM_CAPACITY() -> int:
    return MEM_CAPACITY    

def get_STR_CAPACITY() -> int:
    return STR_CAPACITY    

def get_OPS() -> int: 
    return COUNT_OPS    

def get_OP_PUSH() -> int:
    return OP_PUSH

def get_OP_ADD() -> int:
    return OP_ADD
    
def get_OP_SUB() -> int:
    return OP_SUB

def get_OP_DUMP() -> int:
    return OP_DUMP

def get_OP_EQUAL() -> int:
    return OP_EQUAL

def get_OP_IF() -> int:
    return OP_IF

def get_OP_END() -> int:    
    return OP_END

def get_OP_ELSE() -> int:
    return OP_ELSE

def get_OP_DUP() -> int:
    return OP_DUP

def get_OP_DUP2() -> int:
    return OP_DUP2

def get_OP_GT() -> int:
    return OP_GT

def get_OP_LT() -> int:
    return OP_LT

def get_OP_GE() -> int:
    return OP_GE

def get_OP_LE() -> int:
    return OP_LE    

def get_OP_NE() -> int:
    return OP_NE

def get_OP_DIV() -> int:
    return OP_DIV

def get_OP_MUL() -> int:
    return OP_MUL

def get_OP_DIVMOD() -> int:
    return OP_DIVMOD

def get_OP_WHILE() -> int:
    return OP_WHILE

def get_OP_DO() -> int:
    return OP_DO

def get_OP_MEM() -> int:
    return OP_MEM

def get_OP_LOAD() -> int:
    return OP_LOAD

def get_OP_STORE() -> int:
    return OP_STORE   

def get_OP_SYSCALL0() -> int:
    return OP_SYSCALL0

def get_OP_SYSCALL1() -> int:
    return OP_SYSCALL1

def get_OP_SYSCALL2() -> int:
    return OP_SYSCALL2   

def get_OP_SYSCALL3() -> int:
    return OP_SYSCALL3  


def get_OP_SYSCALL4() -> int:
    return OP_SYSCALL4

def get_OP_SYSCALL5() -> int:
    return OP_SYSCALL5   

def get_OP_SYSCALL6() -> int:
    return OP_SYSCALL6   

def get_OP_EXIT() -> int:
    return OP_EXIT   

def get_OP_WRITE() -> int:
    return OP_WRITE

def get_OP_SWAP() -> int:
    return OP_SWAP   

def get_OP_DROP() -> int:
    return OP_DROP   

def get_OP_SHL() -> int:
    return OP_SHL

def get_OP_SHR() -> int:
    return OP_SHR

def get_OP_ORB() -> int:
    return OP_ORB

def get_OP_ANDB() -> int:
    return OP_ANDB

def get_OP_OVER() -> int:
    return OP_OVER

def get_OP_MOD() -> int:
    return OP_MOD

def get_OP_STRING() -> int:
    return OP_STRING

def get_OP_CHAR() -> int:
    return OP_CHAR

def get_OP_VAR() -> int:
    return OP_VAR

def get_OP_IDVAR() -> int:
    return OP_IDVAR

def get_OP_ASSIGN() -> int:
    return OP_ASSIGN

def get_OP_VARTYPE() -> int:
    return OP_VARTYPE

keyword_table: Dict = {
    PLUS: OP_ADD,
    MINUS: OP_SUB,
    DUMP: OP_DUMP,
    EQUAL: OP_EQUAL,
    OPIF: OP_IF,
    OPEND: OP_END,
    OPELSE: OP_ELSE,
    OPDUP: OP_DUP,
    OPDUP2: OP_DUP2,
    OPGT: OP_GT,
    OPLT: OP_LT,
    OPWHILE: OP_WHILE,
    OPDO: OP_DO,
    OPMEM: OP_MEM,
    OPSTORE: OP_STORE,
    OPLOAD: OP_LOAD,
    OPSYSCALL0: OP_SYSCALL0,
    OPSYSCALL1: OP_SYSCALL1,
    OPSYSCALL2: OP_SYSCALL2,
    OPSYSCALL3: OP_SYSCALL3,
    OPSYSCALL4: OP_SYSCALL4,
    OPSYSCALL5: OP_SYSCALL5,
    OPSYSCALL6: OP_SYSCALL6,
    OPEXIT: OP_EXIT,
    OPWRITE: OP_WRITE,
    OPSWAP: OP_SWAP,
    OPDROP: OP_DROP,
    OPSHL: OP_SHL,
    OPSHR: OP_SHR,
    OPORB: OP_ORB,
    OPANDB: OP_ANDB,
    OPOVER: OP_OVER,
    OPMOD: OP_MOD,
    OPGE: OP_GE,
    OPLE: OP_LE,
    OPNE: OP_NE,
    OPDIV: OP_DIV,
    OPMUL: OP_MUL,
    OPDIVMOD: OP_DIVMOD,
    OPMACRO: OP_MACRO,
    OPENDM: OP_ENDM,
    OPINCLUDE: OP_INCLUDE,
    OPVAR: OP_VAR,
    OPASSIGN: OP_ASSIGN
}

special_chars: Dict = {
    '\\n': '\n',
    '\\t': '\t',
    '\\r': '\r',
    '\\f': '\f',
    '\\v': '\v',
    '\\b': '\b',
    '\\a': '\a',
    '\\0': '\0',
}


#returns the type of the token
def get_token_type(token) -> int:
    if token in keyword_table:
        return keyword_table[token]
    else:
        try:
            int(token)
            return OP_NUMBER
        except ValueError:
            return OP_UNKNOWN    