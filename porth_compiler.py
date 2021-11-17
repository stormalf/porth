#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from porth_lexer import get_OP_ADD, get_OP_GT, get_OP_SUB, get_OP_PUSH, get_OP_DUMP, \
    get_OP_EQUAL, get_OPS, get_OP_IF, get_OP_END, get_OP_ELSE, get_OP_DUP, \
    get_OP_GT, get_OP_LT

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
format db  "%d", 10, 0
'''

#Need to increase the max_ops each time we add a new opcode
MAX_OPS = 13

#simulate the program execution without compiling it
def simulate(program):
    assert get_OPS() == MAX_OPS, "Max Opcode implemented!"
    stack=[]
    error = False
    ip = 0
    #print(program)
    if not error:
        while ip < len(program):
            op = program[ip]
            if op[0]==get_OP_PUSH():
                ip += 1
                stack.append(op[1])
            elif op[0]==get_OP_ADD():
                ip += 1                
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op[0]==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op[0]==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a)) 
            elif op[0]==get_OP_DUMP():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to dump")
                    error = True
                else:
                    a = stack.pop()
                    print(a)
            elif op[0]==get_OP_IF():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to execute if statement")
                    error = True
                else:
                    a = stack.pop()
                    if a == 0:
                        assert len(op) >= 2, "if instruction does not have an End instruction!"
                        ip = op[1]
                        pass
            elif op[0]==get_OP_ELSE():
                ip += 1  
                assert len(op) >= 2, "else instruction does not have an End instruction!"   
                ip = op[1]                      
            elif op[0]==get_OP_END():
                ip += 1
            elif op[0]==get_OP_DUP():
                a = stack.pop()
                stack.append(a)
                stack.append(a)
                ip += 1 
            elif op[0]==get_OP_GT():
                if len(stack) < 2:
                    print("> impossible not enough element in stack")
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(b > a)) 
                ip += 1             
            elif op[0]==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(b < a))                 
                ip += 1                                   
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
    return stack, error  


#compile the bytecode using nasm and gcc (for printf usage)
def compile(bytecode, outfile):
    assert get_OPS() == MAX_OPS, "Max Opcode implemented!"    
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    output.write(HEADER) 
    error = False    
    #print(bytecode)
    for ip in range(len(bytecode)):
        op = bytecode[ip]
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
        elif op[0]==get_OP_IF():
            assert len(op) >= 2, f"compile error! if instruction does not have an End instruction! {op}"            
            output.write("; if \n")
            output.write("pop    rax \n")
            output.write("test    rax, rax \n")
            jumpaddress = op[1]
            output.write(f"jz    addr_{op[1]} \n")
        elif op[0]==get_OP_ELSE(): 
            assert len(op) >= 2, f"compile error! else instruction does not have an End instruction! {op}"
            jumpelse = op[1]
            output.write("; else \n")
            output.write(f"jmp    addr_{op[1]} \n")  
            output.write(f"addr_{ip+1}: \n")    
        elif op[0]==get_OP_END():
            output.write("; end \n")
            output.write(f"addr_{ip}: \n")
        elif op[0]==get_OP_DUMP():
            output.write("pop rax \n")
            output.write("call print\n")   
        elif op[0]==get_OP_DUP():
            output.write("; dup \n")            
            output.write("pop rax \n")
            output.write("push rax\n")               
            output.write("push rax\n")                           
        elif op[0]==get_OP_GT():
            output.write("; gt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovg  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")                
        elif op[0]==get_OP_LT():
            output.write("; lt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovl  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")                  
        else:
            print(f"Unknown bytecode op: {op}")    
            error = True    
    output.write(FOOTER)
    output.close()
    os.system(f"nasm -felf64 {asmfile} &&  gcc {outfile}.o -o {outfile} ")
    return error
