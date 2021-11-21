#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from porth_lexer import get_OP_ADD, get_OP_SUB, get_OP_PUSH, get_OP_DUMP, \
    get_OP_EQUAL, get_OPS, get_OP_IF, get_OP_END, get_OP_ELSE, get_OP_DUP, \
    get_OP_GT, get_OP_LT, get_OP_WHILE, get_OP_DO, get_OP_MEM, get_OP_LOAD, get_OP_STORE, \
    get_OP_SYSCALL1, get_OP_SYSCALL3



#Need to increase the max_ops each time we add a new opcode
MAX_OPS = 20

#max memory size
MEM_CAPACITY = 640_000

#header2 without printf but using syscall to write on the screen
HEADER2 = '''%define SYS_EXIT 60
BITS 64
segment .text
print:
mov r9, -3689348814741910323
sub rsp, 40
mov BYTE [rsp+31], 10
lea rcx, [rsp+30]
.L2:
mov rax, rdi
lea r8, [rsp+32]
mul r9
mov rax, rdi
sub r8, rcx
shr rdx, 3
lea rsi, [rdx+rdx*4]
add rsi, rsi
sub rax, rsi
add eax, 48
mov BYTE [rcx], al
mov rax, rdi
mov rdi, rdx
mov rdx, rcx
sub rcx, 1
cmp rax, 9
ja .L2
lea rax, [rsp+32]
mov edi, 1
sub rdx, rax
xor eax, eax
lea rsi, [rsp+32+rdx]
mov rdx, r8
mov rax, 1
syscall
;call write
add rsp, 40
ret
global _start
_start:
'''

#using printf standard function to print on the screen
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
'''

DATA='''
segment .data 
format db  "%d", 10, 0
'''

BSS=f'''
section .bss    ; uninitialized data section
mem: resb {MEM_CAPACITY}
'''


#simulate the program execution without compiling it
def simulate(program):
    assert get_OPS() == MAX_OPS, "Max Opcode implemented!"
    stack=[]
    error = False
    isMem = False
    ip = 0
    exit_code = 0
    mem = bytearray(MEM_CAPACITY)
    #print(program)
    if not error:
        while ip < len(program):
            #print(stack)
            op = program[ip]
            if op['type']==get_OP_PUSH():
                ip += 1
                stack.append(op['value'])
            elif op['type']==get_OP_ADD():
                ip += 1                
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op['type']==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op['type']==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a)) 
            elif op['type']==get_OP_DUMP():
                ip += 1                
                if len(stack) == 0:
                    # print("stack is empty impossible to dump")
                    # error = True
                    pass
                else:
                    a = stack.pop()
                    print(a)
            elif op['type']==get_OP_IF():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to execute if statement")
                    error = True
                else:
                    a = stack.pop()
                    if a == 0:
                        assert len(op) >= 2, "if instruction does not have an End instruction!"
                        ip = op['jmp']
                        pass
            elif op['type']==get_OP_ELSE():
                #ip += 1  
                assert len(op) >= 2, "else instruction does not have an End instruction!"   
                ip = op['jmp']                      
            elif op['type']==get_OP_END():
                assert len(op) >= 2, "end instruction does not have next instruction to jump check the crossreferences!"                 
                ip = op['jmp']
            elif op['type']==get_OP_DUP():
                a = stack.pop()
                stack.append(a)
                stack.append(a)
                ip += 1 
            elif op['type']==get_OP_GT():
                if len(stack) < 2:
                    print("> impossible not enough element in stack")
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a > b)) 
                ip += 1             
            elif op['type']==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a < b))                 
                ip += 1   
            elif op['type']==get_OP_WHILE():
                ip += 1                
            elif op['type']==get_OP_DO():
                #ip += 1
                a = stack.pop()
                if a == 0:
                    assert len(op) >= 2, "end instruction does not have next instruction to jump, check the crossreferences!"    
                    ip = op['jmp']
                else:
                    ip += 1    
            elif op['type']==get_OP_MEM():
                isMem = True
                stack.append(0)
                ip += 1   
            elif op['type']==get_OP_LOAD():
                addr = stack.pop()
                byte = mem[addr]
                stack.append(byte)
                ip += 1                    
            elif op['type']==get_OP_STORE():
                value = stack.pop()
                addr = stack.pop()
                mem[addr] = value & 0xFF
                ip += 1   
            elif op['type']==get_OP_SYSCALL1():
                syscall_number = stack.pop()
                exit_code = stack.pop()
                if syscall_number == 60:
                    break
                else:
                    print(f"unknown syscall3: {syscall_number}")
                    error = True                
                ip += 1                      
            elif op['type']==get_OP_SYSCALL3():
                syscall_number = stack.pop()
                arg1 = stack.pop()
                arg2 = stack.pop()
                arg3 = stack.pop()
                if syscall_number == 1:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    s = mem[buffer:buffer+count].decode('utf-8')
                    if fd == 1:
                        print(s, end='')
                    elif fd == 2:
                        print(s, end='', file=sys.stderr)
                    else:
                        print(f"unknown file descriptor: {fd}")
                        error = True
                else:
                    print(f"unknown syscall1: {syscall_number}")
                    error = True
                ip += 1                                   
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
        if isMem:
            print(f"memory dump {mem[:20]}")                
    return stack, error, exit_code  


#compile the bytecode using nasm and gcc (for printf usage)
def compile(bytecode, outfile, libc=True):
    assert get_OPS() == MAX_OPS, "Max Opcode implemented!"    
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    if libc:
        output.write(HEADER) 
    else:
        output.write(HEADER2)
    error = False    
    for ip in range(len(bytecode)):
        op = bytecode[ip]
        output.write(f"addr_{ip}: \n")
        if op['type']==get_OP_PUSH():
            output.write("; push \n")             
            output.write(f"push {op['value']}\n")
        elif op['type']==get_OP_ADD():
            output.write("; add \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")
            output.write("add    rax, rbx \n")
            output.write("push    rax \n")
        elif op['type']==get_OP_SUB():
            output.write("; sub \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")
            output.write("sub    rax, rbx \n")                
            output.write("push    rax \n")
        elif op['type']==get_OP_EQUAL():
            output.write("; equal \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmove  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")           
        elif op['type']==get_OP_IF():
            assert len(op) >= 2, f"compile error! IF instruction does not have an END instruction! {op}"            
            output.write("; if \n")
            output.write("pop    rax \n")
            output.write("test    rax, rax \n")
            output.write(f"jz    addr_{op['jmp']} \n")
        elif op['type']==get_OP_ELSE(): 
            assert len(op) >= 2, f"compile error! ELSE instruction does not have an END instruction! {op}"
            output.write("; else \n")
            output.write(f"jmp    addr_{op['jmp']} \n")  
            #output.write(f"addr_{ip+1}: \n")    
        elif op['type']==get_OP_END():
            output.write("; end \n")
            assert len(op) >= 2, f"compile error! END instruction does not have a next instruction to jump! {op}"  
            if ip + 1 != op['jmp']:
                output.write(f"jmp    addr_{op['jmp']} \n")          
        elif op['type']==get_OP_DUMP():
            output.write("; dump \n")
            if libc:
                output.write("pop rax \n")
            else:
                output.write("pop rdi \n")
            output.write("call print\n")   
        elif op['type']==get_OP_DUP():
            output.write("; dup \n")            
            output.write("pop rax \n")
            output.write("push rax\n")               
            output.write("push rax\n")                           
        elif op['type']==get_OP_GT():
            output.write("; gt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovg  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")                
        elif op['type']==get_OP_LT():
            output.write("; lt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovl  rcx, rdx \n")  
            output.write("mov  rax, rcx \n") 
            output.write("push    rax \n")                  
        elif op['type']==get_OP_WHILE():
            output.write("; while \n")
        elif op['type']==get_OP_DO():
            output.write("; do \n") 
            output.write("pop    rax \n")
            output.write("test    rax, rax \n")
            assert len(op) >= 2, f"compile error! DO instruction does not have an END instruction to jump! {op}"             
            output.write(f"jz    addr_{op['jmp']} \n")    
        elif op['type']==get_OP_MEM(): 
            output.write("; mem \n")
            output.write("push mem\n")   
        elif op['type']==get_OP_LOAD(): 
            output.write("; load \n")
            output.write("pop rax\n")    
            output.write("xor rbx, rbx\n")           
            output.write("mov bl, [rax]\n")
            output.write("push rbx\n")
        elif op['type']==get_OP_STORE(): 
            output.write("; store \n")
            output.write("pop rbx\n")
            output.write("pop rax\n")
            output.write("mov [rax], bl\n")
        elif op['type']==get_OP_SYSCALL1():    
            output.write("; syscall1 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")            
            output.write("syscall\n")            
        elif op['type']==get_OP_SYSCALL3():    
            output.write("; syscall3 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")            
            output.write("pop rsi\n")
            output.write("pop rdx\n")            
            output.write("syscall\n")
        else:
            print(f"Unknown bytecode op: {op}")    
            error = True    
    output.write(FOOTER)
    output.write(DATA)
    output.write(BSS)
    output.close()
    if libc:
        os.system(f"nasm -felf64 {asmfile}  &&  gcc -static {outfile}.o -o {outfile} ")
    else:
        os.system(f"nasm -felf64 {asmfile}  &&  ld -static {outfile}.o -o {outfile} ")
    return error
