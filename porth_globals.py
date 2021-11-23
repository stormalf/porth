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
    elif token == OPDUP2:
        return OP_DUP2            
    elif token == OPGT:
        return OP_GT          
    elif token == OPLT:
        return OP_LT    
    elif token == OPWHILE:
        return OP_WHILE   
    elif token == OPDO:
        return OP_DO        
    elif token == OPMEM:
        return OP_MEM  
    elif token == OPSTORE:
        return OP_STORE
    elif token == OPLOAD:
        return OP_LOAD   
    elif token == OPSYSCALL1:
        return OP_SYSCALL1          
    elif token == OPSYSCALL2:
        return OP_SYSCALL2               
    elif token == OPSYSCALL3:
        return OP_SYSCALL3                                                       
    elif token == OPSYSCALL4:
        return OP_SYSCALL4          
    elif token == OPSYSCALL5:
        return OP_SYSCALL5               
    elif token == OPSYSCALL6:
        return OP_SYSCALL6                                                       
    elif token == OPRETURN:
        return OP_RETURN    
    elif token == OPSWAP:
        return OP_SWAP 
    elif token == OPDROP:
        return OP_DROP   
    elif token == OPSHL:
        return OP_SHL   
    elif token == OPSHR:
        return OP_SHR   
    elif token == OPORB:
        return OP_ORB   
    elif token == OPANDB:
        return OP_ANDB                                                    
    elif token == OPOVER:
        return OP_OVER
    elif token == OPMOD:
        return OP_MOD  
    elif token == OPGE:
        return OP_GE  
    elif token == OPLE:
        return OP_LE
    elif token == OPNE:
        return OP_NE  
    elif token == OPDIV:
        return OP_DIV  
    elif token == OPMUL:
        return OP_MUL                                                
    else:       
        try:
            int(token)
            return OP_NUMBER
        except ValueError:
            return OP_UNKNOWN    