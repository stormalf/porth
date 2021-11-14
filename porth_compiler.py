#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from porth_lexer import get_OP_ADD, get_OP_SUB, get_OP_PUSH, get_OP_DUMP, get_OP_EQUAL, get_OPS, add, sub, push, dump, equal

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

#simulate the program execution without compiling it
def simulate(program):
    assert get_OPS() == 5, "Max Opcode implemented!"
    stack=[]
    error = False
    if not error:
        for op in program:
            if op[0]==get_OP_PUSH():
                stack.append(op[1])
            elif op[0]==get_OP_ADD():
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op[0]==get_OP_SUB():
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op[0]==get_OP_EQUAL():
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a))                    
            elif op[0]==get_OP_DUMP():
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
    assert get_OPS() == 5, "Max Opcode implemented!"    
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    output.write(HEADER) 
    error = False    
    for op in bytecode:
        if op[0]==get_OP_PUSH():
            output.write(f"push {op[1]}\n")
        elif op[0]==get_OP_ADD():
            output.write("; add \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")
            output.write("add    rax, rbx \n")
            output.write("push    rax \n")
        elif op[0]==get_OP_SUB():
            output.write("; sub \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")
            output.write("sub    rax, rbx \n")                
            output.write("push    rax \n")
        elif op[0]==get_OP_EQUAL():
            output.write("; equal \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmove  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")           
        elif op[0]==get_OP_DUMP():
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
            if op[0]==get_OP_PUSH():
                bytecode.append(push(op[1]))
            elif op[0]==get_OP_ADD():
                bytecode.append(add())

            elif op[0]==get_OP_SUB():
                bytecode.append(sub())
            elif op[0]==get_OP_DUMP():
                bytecode.append(dump())
            elif op[0]==get_OP_EQUAL():
                bytecode.append(equal())                
            else:
                print(f"Unknown opcode: {op}")    
                error = True
    return bytecode, error
