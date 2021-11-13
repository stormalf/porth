#!/usr/bin/python3
# -*- coding: utf-8 -*-

''' 
python implementation of forth language
tuned for python 3.8 
Following the description of the forth language by Charles H. Moore
http://www.forth.org/
Youtube videos from Tsoding Daily 
'''

import argparse
import os
from porth_lexer import lex_file
__version__ = "1.0.0"


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


def porthVersion():
    return f"porth version : {__version__}"

iota_counter=0

#enum function in python 
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter=0
    else:
        iota_counter+=1
    return iota_counter

OP_PUSH=iota()    
OP_ADD=iota()
OP_SUB=iota()
OP_DUMP=iota()
#keep in last line to have the counter working
COUNT_OPS=iota()

##functions for the porth language
def push(value):
    return (OP_PUSH, value)

def add():
    return (OP_ADD,)

def sub():
    return (OP_SUB,)

def dump():
    return (OP_DUMP,)

#returns the function corresponding to the token found
def parse_word(word):
    #print(word)
    if word == PLUS:
        return add()
    elif word == MINUS:
        return sub()
    elif word == DUMP:
        return dump()
    else:
        try :
            number = int(word)
            return push(number)                    
        except ValueError:
            print(f"Unknown word: {word}")
            return None

#returns the program in the porth language
def load_program(filename):
    with open(filename, "r") as f:
        tokens = f.read().split()
        return [parse_word(word) for word in tokens], tokens
    
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
            else:
                print(f"Unknown opcode: {op}")    
                error = True
    return bytecode, error

def main(args, filename):   
    error = False
    tokens=[]
    bytecode=[]
    program, tokens = load_program(filename)
    if None in program:
        error = True
    if not error and args.simulate:
        print(f"simulating...")
        stack, error = simulate(program)
        if not error:
            #print(f"stack : {stack}")
            print("simulation succeeded!")
        else:
            print("simulation failed!")
    if not error and (args.bytecode or args.compile):
        bytecode, error = generate_bytecode(program)
        if not error:
            print(f"bytecode : {bytecode}")            
            print("bytecode generated!")
        else:
            print("bytecode generation failed!")
            error = True
    if not error and args.compile:
        print(f"compiling...")
        error = compile(bytecode, args.outfile)
        if not error:
            print("compilation done!")
        else:
            print("compilation failed!")    

    if args.dump:
        print(f"dumping...")
        print(f"tokens : {tokens}")
        print(f"stack : {stack}")
        print(f"bytecode : {bytecode}")        
        print("dumping done!")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="porth is a python3 forth language simulation")
    parser.add_argument('-V', '--version', help='Display the version of porth', action='version', version=porthVersion())
    parser.add_argument('-c', '--compile', help='compile', action="store_true", required=False)
    parser.add_argument('-d', '--dump', help='dump', action="store_true", required=False)
    parser.add_argument('-b', '--bytecode', help='generate bytecode', action="store_true", required=False)    
    parser.add_argument('-s', '--simulate', help='simulate', action="store_true", required=False)
    parser.add_argument('-i', '--inputfile', help='intput file', required=True)
    parser.add_argument('-o', '--outfile', help='output file', default="output", required=False)
    args = parser.parse_args()
    #program=[push(51), push(32), add(), dump(), push(528), push(140), sub(), dump()]
    program = args.inputfile
    main(args, program)
