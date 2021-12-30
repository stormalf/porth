#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import *

#Need to increase the max_ops each time we add a new opcode
MAX_OPS = 67
MAX_ERROR_TABLE = 35
MAX_WARNING_TABLE=1

BUFFER_SIZE = 2048

#max memory size
NULL_POINTER_PADDING = 1
MEM_CAPACITY = 640_000
STR_CAPACITY = 640_000
ARGV_CAPACITY = 640_000

MAX_LOOP_SECURITY = 10_000_000

#max min values
MAX_U8 = 255
MAX_U16 = 65535
MAX_U32 = 4294967295
MAX_U64 = 18446744073709551615

MIN_U8 = 0
MIN_U16 = 0
MIN_U32 = 0
MIN_U64 = 0

MAX_I8 = 127
MAX_I16 = 32767
MAX_I32 = 2147483647
MAX_I64 = 9223372036854775807
MIN_I8 = -128
MIN_I16 = -32768
MIN_I32 = -2147483648
MIN_I64 = -9223372036854775808

MIN_BOOL = 0
MAX_BOOL = 1

MIN_PTR = NULL_POINTER_PADDING
MAX_PTR = NULL_POINTER_PADDING + STR_CAPACITY + ARGV_CAPACITY + MEM_CAPACITY

#struct 
var_struct = {}
macro_struct= {}
warning_msg = {}
error_msg = {}
files_struct = {}
include_file=[]
runtime_msg = {}


iota_counter= 0
exit_code = 0
error_counter = 0
stack_counter = 0
warning_counter = 0
error_table_counter = 0
warning_table_counter = 0

#list of comments types probably I'll prefer the python comment syntax for myself
#I keep only two // and # I removed the ; perhaps we need it later for other operation code
#COMMENTS = ["//", "#", ";"]
COMMENTS = ["//", "#"]

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
#STRING_LITERAL = [DOUBLE_QUOTE, " "]

reserved_words = ["_format", "_format2", "_negative", "_security", "_file", "_options", "_fd", "_mem", "_char", "_open", \
    "_close", "print", ".L2", "print_char", "_start", "main", "print_error", ".bss", ".data", ".text", "_file_buffer", "_write_buffer" \
        "_int_to_string", ".push_chars", ".pop_chars"]


#files mode
O_ACCMODE = 3
O_RDONLY = 0
O_WRONLY = 1
O_RDWR = 2
O_CREAT = 100
O_EXCL = 200
O_NOCTTY = 400
O_TRUNC = 1000
O_APPEND = 2000
O_NONBLOCK = 4000
O_DSYNC = 10000
O_FASYNC = 20000
O_DIRECT = 40000
O_LARGEFILE = 100000
O_DIRECTORY = 200000
O_NOFOLLOW = 400000
O_NOATIME = 1000000
O_CLOEXEC = 2000000

#returns the number of warnings found
def get_stack_counter() -> int:
    global stack_counter
    return stack_counter    

def set_stack_counter(value: int = 1) -> None:
    global stack_counter
    stack_counter += value

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

def get_var_type(var: Union[str, int]) -> Union[str, None]:
    global var_struct
    if var in var_struct:
        return var_struct[var]['type']
    else:
        return None        

def get_var_qualifier(type: str) -> str:
    if type in (OPU8, OPI8, OPBOOL):
        return "byte"
    elif type in(OPU16, OPI16):
        return "word"
    elif type in (OPU32, OPI32):
        return "dword"
    elif type in (OPU64, OPI64, OPPTR):
        return "qword"

def get_register(type: str) -> str:
    if type in (OPU8, OPI8, OPBOOL):
        return "al"
    elif type in(OPU16, OPI16):
        return "ax"
    elif type in(OPU32, OPI32):
        return "eax"
    elif type in(OPU64, OPI64, OPPTR):
        return "rax"

def check_valid_value(type: str, value: int) -> bool:
    isValid = True
    if type == OPU8 and (value < MIN_U8 or value > MAX_U8) :
        isValid = False
    elif type == OPU16 and (value < MIN_U16 or value > MAX_U16):
        isValid = False
    elif type == OPU32 and (value < MIN_U32 or value > MAX_U32):
        isValid = False
    elif type == OPU64 and (value < MIN_U64 or value > MAX_U64):
        isValid = False        
    elif type == OPI8 and (value < MIN_I8 or value > MAX_I8):
        isValid = False
    elif type == OPI16 and (value < MIN_I16 or value > MAX_I16):
        isValid = False
    elif type == OPI32 and (value < MIN_I32 or value > MAX_I32):
        isValid = False
    elif type == OPI64 and (value < MIN_I64 or value > MAX_I64):
        isValid = False
    elif type == OPBOOL and (value < MIN_BOOL or value > MAX_BOOL):
        isValid = False
    elif type == OPPTR and (value < MIN_PTR or value > MAX_PTR):
        isValid = False
    return isValid

def check_file_closed(fd: int) -> bool:
    global files_struct
    if fd in files_struct:
        return files_struct[fd]['close']
    else:
        return False


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
#OP_ASSIGN=iota()
OP_IDVAR=iota()
OP_VARTYPE=iota()
OP_ASSIGN_VAR=iota()
OP_LOAD16=iota()
OP_STORE16=iota()
OP_LOAD32=iota()
OP_STORE32=iota()
OP_LOAD64=iota()
OP_STORE64=iota()
OP_ARGC=iota()
OP_ARGV=iota()
OP_ROTATE=iota()
OP_OPEN=iota()
OP_CLOSE=iota()
OP_OPENW=iota()
OP_READF=iota()
OP_WRITEF=iota()
OP_ITOS=iota()

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
ERR_TOK_ITOS=iota()
ERR_VAR_UNDEF=iota()
ERR_VAR_ASSIGN=iota()
ERR_VAR_TYPE=iota()
ERR_VAR_DEF=iota()
ERR_VAR_NOT_ALW=iota()

#warning code 
WARN_NO_WARNING=iota(True)
WARN_VAR_UNUSED=iota()
WARN_STACK_NOTEMPTY=iota()

#error codes runtime
RUN_NO_ERROR=iota(True)
RUN_DIV_ZERO=iota()
RUN_UNKNOWN=iota()
RUN_INFINITE_LOOP=iota()
RUN_STK_ERR=iota()
RUN_JMP_ERR=iota()
RUN_SYSCALL_ERR=iota()
RUN_NOTYET_ERR=iota()
RUN_MEM_ERR=iota()
RUN_FILE_ERR=iota()
RUN_VAR_ERR=iota()

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
OPOR="OR"
OPANDB="ANDB"
OPAND="AND"
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
OPASSIGNVAR= OPASSIGN + OPIDVAR
OPS8="@8"
OPL8="$8"
OPS16="@16"
OPL16="$16"
OPS32="@32"
OPL32="$32"
OPS64="@64"
OPL64="$64"
OPARGC="ARGC"
OPARGV="ARGV"
OPROTATE="ROT"
OPOPEN="OPEN"
OPCLOSE="CLOSE"
OPOPENW="OPENW"
OPREADF="READF"
OPWRITEF="WRITEF"
OPBOOL='bool'
OPI8="i8"
OPI16="i16"
OPI32="i32"
OPI64="i64"
OPITOS="ITOS" #convert int to string return into stack the length and the address of the string
OPPTR="ptr"
# OPF32="f32"
# OPF64="f64"
# OPSTRING="str"
# OPCHAR="char"

OPERATORS=[OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_SHL, OP_SHR, OP_ANDB, OP_ORB, OP_MOD]

VAR_TYPE=[OPU8,OPU16,OPU32,OPU64, OPBOOL, OPI8, OPI16, OPI32, OPI64, OPPTR]

#forbidden_tokens = [PLUS, MINUS, DUMP]

def get_MAX_ERROR() -> int:
    return MAX_ERROR_TABLE    

def get_MAX_WARNING() -> int:
    return MAX_WARNING_TABLE    

def get_MAX_OPS() -> int:
    return MAX_OPS    

def get_MEM_CAPACITY() -> int:
    return MEM_CAPACITY    

def get_STR_CAPACITY() -> int:
    return STR_CAPACITY    

def get_ARGV_CAPACITY() -> int:
    return ARGV_CAPACITY

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

def get_OP_LOAD8() -> int:
    return OP_LOAD

def get_OP_STORE8() -> int:
    return OP_STORE   

def get_OP_LOAD16() -> int:
    return OP_LOAD16

def get_OP_STORE16() -> int:
    return OP_STORE16

def get_OP_LOAD32() -> int:
    return OP_LOAD32

def get_OP_STORE32() -> int:
    return OP_STORE32

def get_OP_LOAD64() -> int:
    return OP_LOAD64

def get_OP_STORE64() -> int:
    return OP_STORE64  

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

def get_OP_OR() -> int:
    return OP_ORB

def get_OP_AND() -> int:
    return OP_ANDB

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

# def get_OP_ASSIGN() -> int:
#     return OP_ASSIGN

def get_OP_VARTYPE() -> int:
    return OP_VARTYPE

def get_OP_ASSIGN_VAR() -> int:
    return OP_ASSIGN_VAR

def get_OP_ARGC() -> int:
    return OP_ARGC

def get_OP_ARGV() -> int:
    return OP_ARGV

def get_OP_ROTATE() -> int:
    return OP_ROTATE

def get_OP_OPEN() -> int:
    return OP_OPEN

def get_OP_CLOSE() -> int:
    return OP_CLOSE

def get_OP_OPENW() -> int:
    return OP_OPENW

def get_OP_READF() -> int:
    return OP_READF

def get_OP_WRITEF() -> int:
    return OP_WRITEF

def get_OP_ITOS() -> int:
    return OP_ITOS

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
    OPL8: OP_LOAD,
    OPS8: OP_STORE,
    OPS16: OP_STORE16,
    OPL16: OP_LOAD16,
    OPS32: OP_STORE32,
    OPL32: OP_LOAD32,
    OPS64: OP_STORE64,
    OPL64: OP_LOAD64,
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
    OPOR: OP_ORB,
    OPAND: OP_ANDB,
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
    OPARGC: OP_ARGC,
    OPARGV: OP_ARGV,
    OPROTATE: OP_ROTATE,
    OPOPEN: OP_OPEN,
    OPCLOSE: OP_CLOSE,
    OPOPENW: OP_OPENW,
    OPREADF: OP_READF,
    OPWRITEF: OP_WRITEF,
    OPITOS: OP_ITOS
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