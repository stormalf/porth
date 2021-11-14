#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

#header assembly that contains the printf call function
HEADER = '''%define SYS_EXIT 60\n
BITS 64
segment .text
global main
extern printf
print:
        mov     rdi, format             ; set 1st parameter (format)
        mov     rsi, rax                ; set 2nd parameter (current_number)
        xor     rax, rax                ; because printf is varargs

        ; Stack is already aligned because we pushed three 8 byte registers
        call    printf   WRT ..plt               ; printf(format, current_number)
        ret
main:\n'''

#footer assembly that exit function followed by data section with format
FOOTER = '''mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%20ld", 10, 0
'''


#tokens digits and 3 operators for now
PLUS= "+"
MINUS = "-"
DUMP = "."
EQUAL = "="

forbidden_tokens = [PLUS, MINUS, DUMP]

iota_counter= 0
error_counter = 0

def get_counter_error():
    return error_counter

# tokenize a file
def lex_file(filename):
    with open(filename, "r") as f:
        return [(filename, row, col, token ) for (row, line) in enumerate(f.readlines(), 1) for (col, token) in lex_line(line)]

#tokenize a line
def lex_line(line):
    tokens = line.split()
    coltok= [] 
    # to manage duplicated tokens in a line
    start = 0
    for token in tokens:
        col = line[start:].find(token) 
        start= col + start + 1  #adding 1 to start from column 1 instead of 0
        coltok.append((start, token))
    return coltok


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
#keep in last line to have the counter working
COUNT_OPS=iota()

NO_ERROR=iota(True)
ERR_TOK_UNKNOWN = iota()
ERR_TOK_FORBIDDEN = iota()


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

def check_first_token(token, forbidden_tokens):
    isOK = False
    if token in forbidden_tokens:
        isOK = True
    return isOK


#returns the function corresponding to the token found
def parse_word(token):
    global error_counter
    #print(word)
    filename, line, column, word = token

    if word == PLUS:
        return add()
    elif word == MINUS:
        return sub()
    elif word == DUMP:
        return dump()
    elif word == EQUAL:
        return equal()        
    else:
        try :
            number = int(word)
            return push(number)                    
        except ValueError:
            print(f"Error Code {ERR_TOK_UNKNOWN} Unknown word: {word} at line {line}, column {column} in file {filename}")
            error_counter += 1
            return (None, None, None, None)

#returns the program in the porth language
def load_program(filename):
    global error_counter
    tokens = lex_file(filename)
    isOK = True
    current_line = 0
    first_token = False
    for token in tokens:
        filename, line, col, tok = token
        if line != current_line:
            first_token = True            
            current_line = line
        if check_first_token(tok, forbidden_tokens) and first_token:
            print(f"Error Code {ERR_TOK_FORBIDDEN} Token {tok} is forbidden in first position in file {filename}, line {line} column {col}")
            error_counter += 1
            first_token = False
            isOK = False
        first_token = False    

    return [parse_word(word) for word in tokens], tokens, isOK
    
#simulate the program execution without compiling it
def simulate(program):
    assert COUNT_OPS == 5, "Max Opcode implemented!"
    stack=[]
    error = False
    if not error:
        for op in program:
            if op[0]==OP_PUSH:
                stack.append(op[1])
            elif op[0]==OP_ADD:
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op[0]==OP_SUB:
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op[0]==OP_EQUAL:
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a))                    
            elif op[0]==OP_DUMP:
                if len(stack) == 0:
                    print("stack is empty")
                    error = True
                else:
                    a = stack.pop()
                    print(a)
            else:
                error = True
                print(f"Unknown opcode: {op}")  
    return stack, error  

#compile the bytecode using nasm and gcc (for printf usage)
def compile(bytecode, outfile):
    assert COUNT_OPS == 5, "Max Opcode implemented!"    
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    output.write(HEADER) 
    error = False    
    for op in bytecode:
        if op[0]==OP_PUSH:
            output.write(f"push {op[1]}\n")
        elif op[0]==OP_ADD:
            output.write("; add \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")
            output.write("add    rax, rbx \n")
            output.write("push    rax \n")
        elif op[0]==OP_SUB:
            output.write("; sub \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")
            output.write("sub    rax, rbx \n")                
            output.write("push    rax \n")
        elif op[0]==OP_EQUAL:
            output.write("; equal \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmove  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")           
        elif op[0]==OP_DUMP:
            output.write("call print\n")   
        else:
            print(f"Unknown bytecode op: {op}")    
            error = True    
    output.write(FOOTER)
    output.close()
    os.system(f"nasm -felf64 {asmfile} &&  gcc {outfile}.o -o {outfile} ")
    return error

#generate the bytecode  
def generate_bytecode(program):
    bytecode=[]
    error = False
    if not error:    
        for op in program:
            if op[0]==OP_PUSH:
                bytecode.append(push(op[1]))
            elif op[0]==OP_ADD:
                bytecode.append(add())

            elif op[0]==OP_SUB:
                bytecode.append(sub())
            elif op[0]==OP_DUMP:
                bytecode.append(dump())
            elif op[0]==OP_EQUAL:
                bytecode.append(equal())                
            else:
                print(f"Unknown opcode: {op}")    
                error = True
    return bytecode, error
