#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Need to increase the max_ops each time we add a new opcode
MAX_OPS = 39

#max memory size
MEM_CAPACITY = 640_000

exit_code = 0


#list of comments types probably I'll prefer the python comment syntax for myself
COMMENTS = ["//", "#", ";"]

iota_counter= 0
error_counter = 0

#enum function in python 
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter=0
    else:
        iota_counter+=1
    return iota_counter

def get_counter_error():
    return error_counter
    
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
OP_WHILE=iota()
OP_DO=iota()
OP_MEM=iota()
OP_LOAD=iota()
OP_STORE=iota()
OP_SYSCALL1=iota()
OP_SYSCALL2=iota()
OP_SYSCALL3=iota()
OP_SYSCALL4=iota()
OP_SYSCALL5=iota()
OP_SYSCALL6=iota()
OP_DUP2=iota()
OP_RETURN=iota()
OP_SWAP=iota()
OP_DROP=iota()
OP_SHL=iota()
OP_SHR=iota()
OP_ORB=iota()
OP_ANDB=iota()
OP_OVER=iota()
OP_MOD=iota()
#keep in last line to have the counter working
COUNT_OPS=iota()

#error codes
NO_ERROR=iota(True)
ERR_TOK_UNKNOWN = iota()
ERR_TOK_FORBIDDEN = iota()
ERR_TOK_BLOCK = iota()
ERR_DIV_ZERO = iota()


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
OPDUP2="2DUP"
OPGT = ">"
OPLT = "<"
OPGE=">="
OPLE="<="
OPNE="!="
OPDIV= "DIV"
OPMUL="MUL"
OPWHILE = "WHILE"
OPDO = "DO"
OPMEM = "MEM"
OPLOAD= "$"
OPSTORE="@"
OPSYSCALL1="SYSCALL1"
OPSYSCALL2="SYSCALL2"
OPSYSCALL3="SYSCALL3"
OPSYSCALL4="SYSCALL4"
OPSYSCALL5="SYSCALL5"
OPSYSCALL6="SYSCALL6"
OPRETURN="RETURN"
OPSWAP="SWAP"
OPDROP="DROP"
OPSHL="SHL"
OPSHR="SHR"
OPORB= "ORB"
OPANDB="ANDB"
OPOVER="OVER"
OPMOD="MOD"


forbidden_tokens = [PLUS, MINUS, DUMP]

def get_MAX_OPS():
    return MAX_OPS    

def get_MEM_CAPACITY():
    return MEM_CAPACITY    

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

def get_OP_DUP2():
    return OP_DUP2

def get_OP_GT():
    return OP_GT

def get_OP_LT():
    return OP_LT

def get_OP_GE():
    return OP_GE

def get_OP_LE():
    return OP_LE    

def get_OP_NE():
    return OP_NE

def get_OP_DIV():
    return OP_DIV

def get_OP_MUL():
    return OP_MUL

def get_OP_WHILE():
    return OP_WHILE

def get_OP_DO():
    return OP_DO

def get_OP_MEM():
    return OP_MEM

def get_OP_LOAD():
    return OP_LOAD

def get_OP_STORE():
    return OP_STORE    

def get_OP_SYSCALL1():
    return OP_SYSCALL1

def get_OP_SYSCALL2():
    return OP_SYSCALL2   

def get_OP_SYSCALL3():
    return OP_SYSCALL3  


def get_OP_SYSCALL4():
    return OP_SYSCALL4

def get_OP_SYSCALL5():
    return OP_SYSCALL5   

def get_OP_SYSCALL6():
    return OP_SYSCALL6   

def get_OP_RETURN():
    return OP_RETURN   

def get_OP_SWAP():
    return OP_SWAP   

def get_OP_DROP():
    return OP_DROP   

def get_OP_SHL():
    return OP_SHL

def get_OP_SHR():
    return OP_SHR

def get_OP_ORB():
    return OP_ORB

def get_OP_ANDB():
    return OP_ANDB

def get_OP_OVER():
    return OP_OVER

def get_OP_MOD():
    return OP_MOD

def get_ERR_DIV_ZERO():
    return ERR_DIV_ZERO
    
keyword_table = {
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
    OPSYSCALL1: OP_SYSCALL1,
    OPSYSCALL2: OP_SYSCALL2,
    OPSYSCALL3: OP_SYSCALL3,
    OPSYSCALL4: OP_SYSCALL4,
    OPSYSCALL5: OP_SYSCALL5,
    OPSYSCALL6: OP_SYSCALL6,
    OPRETURN: OP_RETURN,
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
    OPMUL: OP_MUL

}


#returns the type of the token
def get_token_type(token):
    if token in keyword_table:
        return keyword_table[token]
    else:
        try:
            int(token)
            return OP_NUMBER
        except ValueError:
            return OP_UNKNOWN    