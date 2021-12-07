#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from porth_globals import *

#DIV_BY_0="Division by zero!"


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
print_char:
    push   rbp
    mov    rbp, rsp
    sub    rsp, 16
    mov    rax, rdi
    mov    [rbp - 4], al
    lea    rsi, [rbp - 4]
    mov    rdx, 1
    mov    rdi, 1
    mov    rax, 1
    syscall
    add rsp, 16
    pop    rbp
    ret
global _start
_start:
'''

#using printf standard function to print on the screen
HEADER = f'''%define SYS_EXIT 60\n
BITS 64
segment .text
global main
extern printf, fflush 
print_char:
    mov     rdi, char             ; set 1st parameter (format)
    mov     rsi, rax 
    call printf 
    xor    rdi, rdi                ; clear rdi
    call    fflush 
    ret
print_error:
    call printf 
    xor    rdi, rdi                ; clear rdi
    call    fflush  
    ret
print:
    mov     rdi, format             ; set 1st parameter (format)
    mov     rsi, rax                ; set 2nd parameter (current_number)
    xor     rax, rax                ; because printf is varargs
    call    printf                ; printf(format, current_number)
    xor     rax, rax                ; clear rax
    xor    rdi, rdi                ; clear rdi
    call    fflush             ; fflush(stdout) without it, the output is not printed!!!!!
    ret
main:
'''

#footer assembly that exit function followed by data section with format
FOOTER = f'''mov rax, SYS_EXIT
mov rdi, 0
syscall
'''

DATA=f'''
section .data 
format db  "%llu", 10, 0
char db  "%c", 0
security  dq  {MAX_LOOP_SECURITY}
'''

BSS=f'''
section .bss    ; uninitialized data section
mem: resb {get_MEM_CAPACITY()}
'''




#compile the bytecode using nasm and gcc (for printf usage)
def compile(bytecode: List, outfile: str, libc: bool = True):
    global exit_code, var_struct
    bss_var = []
    strs = []
    assert get_OPS() == get_MAX_OPS(), "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())   
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    if libc:
        output.write(HEADER) 
    else:
        output.write(HEADER2)
    error = False    
    for ip in range(len(bytecode)):
        op = bytecode[ip]
        #print(op)
        output.write(f"addr_{ip}: \n")
        if op['type']==get_OP_PUSH():
            output.write("; push \n")   
            output.write("xor rax, rax\n")
            output.write(f"mov rax, {op['value']}\n")                      
            output.write("push rax\n")
        elif op['type']==get_OP_ADD():
            output.write("; add \n")
            output.write("pop    rax \n")
            output.write("pop    rcx \n")
            output.write("add    rax, rcx \n")
            output.write("push    rax \n")
        elif op['type']==get_OP_SUB():
            output.write("; sub \n")
            output.write("pop    rcx \n")
            output.write("pop    rax \n")
            output.write("sub    rax, rcx \n")                
            output.write("push    rax \n")
        elif op['type']==get_OP_EQUAL():
            output.write("; equal \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rax \n")
            output.write("pop    rbx \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmove  rcx, rdx \n")  
            output.write("push    rcx \n")           
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
        elif op['type']==get_OP_DUP2():
            output.write("; 2dup \n")            
            output.write("pop rcx \n")
            output.write("pop rax \n")            
            output.write("push rax\n")               
            output.write("push rcx\n") 
            output.write("push rax\n")               
            output.write("push rcx\n")                           
        elif op['type']==get_OP_GT():
            output.write("; gt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovg  rcx, rdx \n")  
            output.write("push    rcx \n")                
        elif op['type']==get_OP_LT():
            output.write("; lt \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovl  rcx, rdx \n")  
            output.write("push    rcx \n")  
        elif op['type']==get_OP_GE():
            output.write("; ge \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovge rcx, rdx \n")  
            output.write("push    rcx \n")
        elif op['type']==get_OP_LE():
            output.write("; le \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovle rcx, rdx \n")  
            output.write("push    rcx \n")
        elif op['type']==get_OP_NE():
            output.write("; ne \n")
            output.write("mov    rcx, 0 \n")
            output.write("mov    rdx, 1 \n")
            output.write("pop    rbx \n")
            output.write("pop    rax \n")            
            output.write("cmp    rax, rbx \n")                
            output.write("cmovne rcx, rdx \n")  
            output.write("push    rcx \n")
        elif op['type']==get_OP_DIV():
            output.write("; div \n")
            output.write("pop    rcx \n")
            output.write("pop    rax \n")
            output.write("mov    rdx, 0 \n")
            output.write("cmp rcx, 0\n")
            output.write(f"je addr_div_zero_{ip}\n")
            output.write("div rcx\n")
            output.write("push rax\n")
            output.write(f"jmp addr_div_end_{ip}\n")
            output.write(f"addr_div_zero_{ip}:\n")
            #print the error message using printf if libc
            if libc:
                output.write(f"mov rsi, {len(RUNTIME_ERROR[RUN_DIV_ZERO])}\n")
                output.write(f"mov rdi, error_message_{RUN_DIV_ZERO}\n")    
                output.write("push rdi\n")      
                output.write("push rsi\n")
                output.write("call print_error\n")
            #otherwise print using write syscall
            else:
                output.write("; syscall3 \n")
                output.write("mov rax, 1\n")
                output.write("mov rdi, 1\n")
                output.write(f"mov rdx, {len(RUNTIME_ERROR[RUN_DIV_ZERO]) + 1}\n")            
                output.write(f"mov rsi, error_message_{RUN_DIV_ZERO}\n")            
                output.write("syscall\n")  
            output.write("mov rax, SYS_EXIT\n")
            output.write(f"mov rdi, {RUN_DIV_ZERO}\n")            
            output.write("syscall\n")  
            output.write(f"addr_div_end_{ip}:\n")  
        elif op['type']==get_OP_DIVMOD():
            output.write("; mod \n")
            output.write("xor rdx, rdx\n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("cmp rcx, 0\n")
            output.write(f"je addr_divmod_zero_{ip}\n")
            output.write("div rcx\n")
            output.write("push rdx\n")
            output.write("push rax\n")            
            output.write(f"jmp addr_divmod_end_{ip}\n")
            output.write(f"addr_divmod_zero_{ip}:\n")
            #print the error message using printf if libc
            if libc:
                output.write(f"mov rsi, {len(RUNTIME_ERROR[RUN_DIV_ZERO])}\n")
                output.write(f"mov rdi, error_message_{RUN_DIV_ZERO}\n")    
                output.write("push rdi\n")      
                output.write("push rsi\n")
                output.write("call print_error\n")
            #otherwise print using write syscall
            else:
                output.write("; syscall3 \n")
                output.write("mov rax, 1\n")
                output.write("mov rdi, 1\n")
                output.write(f"mov rdx, {len(RUNTIME_ERROR[RUN_DIV_ZERO]) + 1}\n")            
                output.write(f"mov rsi, error_message_{RUN_DIV_ZERO}\n")            
                output.write("syscall\n")  
            output.write("mov rax, SYS_EXIT\n")
            output.write(f"mov rdi, {RUN_DIV_ZERO}\n")            
            output.write("syscall\n")  
            output.write(f"addr_divmod_end_{ip}:\n")              
        elif op['type']==get_OP_MUL(): 
            output.write("; mul \n")
            output.write("pop    rcx \n")
            output.write("pop    rax \n")
            output.write("imul   rcx \n")
            output.write("push    rax \n")
        elif op['type']==get_OP_WHILE():
            output.write("; while \n")
        elif op['type']==get_OP_DO():
            output.write("; do \n") 
            #adding security for infinite loops I defined 1_000_000
            output.write("mov rcx, [security]\n")
            output.write("dec rcx\n")
            output.write("mov [security], rcx\n")
            output.write("jz infinite_loop\n")            
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
        elif op['type']==get_OP_SWAP(): 
            output.write("; swap \n") 
            output.write("pop rax\n")
            output.write("pop rcx\n")
            output.write("push rax\n")
            output.write("push rcx\n")
        elif op['type']==get_OP_DROP():
            output.write("; drop \n")
            output.write("pop rax\n")
        elif op['type']==get_OP_SHL():
            output.write("; shl \n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("shl rax, cl\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SHR():
            output.write("; shr \n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("shr rax, cl\n")
            output.write("push rax\n")
        elif op['type']==get_OP_ORB():
            output.write("; orb \n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("or rax, rcx\n")
            output.write("push rax\n")
        elif op['type']==get_OP_ANDB():
            output.write("; andb \n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("and rax, rcx\n")
            output.write("push rax\n")
        elif op['type']==get_OP_OVER():
            output.write("; over \n")
            output.write("pop rax\n")
            output.write("pop rcx\n")
            output.write("push rcx\n")
            output.write("push rax\n")
            output.write("push rcx\n")
        elif op['type']==get_OP_MOD():
            output.write("; mod \n")
            output.write("xor rdx, rdx\n")
            output.write("pop rcx\n")
            output.write("pop rax\n")
            output.write("cmp rcx, 0\n")
            output.write(f"je addr_mod_zero_{ip}\n")
            output.write("div rcx\n")
            output.write("push rdx\n")
            output.write(f"jmp addr_mod_end_{ip}\n")
            output.write(f"addr_mod_zero_{ip}:\n")
            #print the error message using printf if libc
            if libc:
                output.write(f"mov rsi, {len(RUNTIME_ERROR[RUN_DIV_ZERO])}\n")
                output.write(f"mov rdi, error_message_{RUN_DIV_ZERO}\n")    
                output.write("push rdi\n")      
                output.write("push rsi\n")                
                output.write("call print_error\n")
            #otherwise print using write syscall
            else:
         
                output.write("; syscall3 \n")
                output.write("mov rax, 1\n")
                output.write("mov rdi, 1\n")
                output.write(f"mov rdx, {len(RUNTIME_ERROR[RUN_DIV_ZERO]) + 1}\n")            
                output.write(f"mov rsi, error_message_{RUN_DIV_ZERO}\n")            
                output.write("syscall\n")  
            output.write("mov rax, SYS_EXIT\n")
            output.write(f"mov rdi, {RUN_DIV_ZERO}\n")            
            output.write("syscall\n")  
            output.write(f"addr_mod_end_{ip}:\n")
        elif op['type']==get_OP_EXIT(): 
            output.write("; exit \n")
            output.write("mov rax, SYS_EXIT\n")
            output.write("pop rdi\n")            
            output.write("syscall\n") 
        elif op['type']==get_OP_WRITE():
            if bytecode[ip - 1]['type']==get_OP_CHAR():
                output.write("; write char \n")
                if libc:
                    output.write(f"mov rax, {bytecode[ip - 1]['value']}\n")
                    output.write("push rax\n")
                    output.write("call print_char\n")
                else:
                    output.write(f"mov rdi, {bytecode[ip - 1]['value']}\n")
                    output.write("push rdi\n")
                    output.write("call print_char\n")

            else:
                output.write("; write \n")
                output.write("mov rax, 1\n")
                output.write("mov rdi, 1\n") 
                output.write("pop rsi\n")
                output.write("pop rdx\n")
                output.write("lea rcx, [rsi]\n")
                output.write("mov rsi, rcx\n")
                output.write("syscall\n")
        elif op['type']==get_OP_SYSCALL0():
            output.write("; syscall0 \n")
            output.write("pop rax\n")
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SYSCALL1():    
            output.write("; syscall1 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")            
            output.write("syscall\n") 
            output.write("push rax\n") 
        elif op['type']==get_OP_SYSCALL2():
            output.write("; syscall2 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")
            output.write("pop rsi\n")
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SYSCALL3():    
            output.write("; syscall3 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")            
            output.write("pop rsi\n")
            output.write("pop rdx\n")            
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SYSCALL4():
            output.write("; syscall4 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")
            output.write("pop rsi\n")
            output.write("pop rdx\n")
            output.write("pop r10\n")
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SYSCALL5():
            output.write("; syscall5 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")
            output.write("pop rsi\n")
            output.write("pop rdx\n")
            output.write("pop r10\n")
            output.write("pop r8\n")
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_SYSCALL6():
            output.write("; syscall6 \n")
            output.write("pop rax\n")
            output.write("pop rdi\n")
            output.write("pop rsi\n")
            output.write("pop rdx\n")
            output.write("pop r10\n")
            output.write("pop r8\n")
            output.write("pop r9\n")
            output.write("syscall\n")
            output.write("push rax\n")
        elif op['type']==get_OP_CHAR():
            output.write("; char\n")  
            output.write(f"push {op['value']}\n")
        elif op['type']==get_OP_STRING():
            output.write("; string \n")
            output.write(f"mov rax, {len(op['value'])}\n")
            #print(len(op['value']), strs)
            output.write("push rax\n")
            output.write(f"push str_{len(strs)}\n")
            strs.append(op['value'])
        elif op['type']==get_OP_VAR():
            pass
        elif op['type']==get_OP_IDVAR():
            #if it's not the definition of a variable, we push the value
            if bytecode[ip - 1]['type'] != get_OP_VAR():
                value = var_struct[op['value']]['value']
                if value != None:
                    output.write("; idvar \n")
                    type=get_var_type(op['value'])
                    qualifier=get_var_qualifier(type)
                    register=get_register(type)
                    #print(f"{op['value']} {type} {qualifier} {register}")
                    #output.write(f"mov {register}, {qualifier} [{op['value']}]\n")
                    output.write(f"xor rax, rax\n")
                    output.write(f"mov {register},  {qualifier} [{op['value']}]\n")
                    #output.write(f"mov rax,  [{op['value']}]\n")
                    output.write(f"push rax\n")
            # #definition of variable we push the address of the variable
            # else:
            #     output.write("; definition idvar \n")
            #     output.write(f"mov rax, [{op['value']}]\n")
            #     output.write("push rax\n")
            pass
        elif op['type']==get_OP_ASSIGN():            
            #output.write("; assign \n")
            # output.write("pop rcx\n") #value or variable 
            # output.write("pop rax\n") #variable
            # output.write("mov [rax], rcx\n")
            pass
            #output.write("push rcx\n") #push address
        elif op['type']==get_OP_VARTYPE():
            pass
        else:
            print(f"Unknown bytecode op: {op}")    
            error = True 
    #managing infinite loop exit (one label only)
    output.write(f"jmp addr_{len(bytecode)}\n")      
    output.write("infinite_loop: \n")
    if libc:
        output.write(f"mov rsi, {len(RUNTIME_ERROR[RUN_INFINITE_LOOP])}\n")
        output.write(f"mov rdi, error_message_{RUN_INFINITE_LOOP}\n")    
        output.write("push rdi\n")      
        output.write("push rsi\n")
        output.write("call print_error\n")
    #otherwise print using write syscall
    else:
        output.write("; syscall3 \n")
        output.write("mov rax, 1\n")
        output.write("mov rdi, 1\n")
        output.write(f"mov rdx, {len(RUNTIME_ERROR[RUN_INFINITE_LOOP]) + 1}\n")            
        output.write(f"mov rsi, error_message_{RUN_INFINITE_LOOP}\n")            
        output.write("syscall\n")
        output.write("mov rax, SYS_EXIT\n")
        output.write(f"mov rdi, {RUN_INFINITE_LOOP}\n")            
        output.write("syscall\n")                             
    output.write(f"addr_{len(bytecode)}:\n")               
    output.write(FOOTER)
    output.write(DATA)
    for index, s in enumerate(strs):
        output.write(f"str_{index}: db {','.join(map(hex, list(bytes(s, 'utf-8'))))}, 0\n")
    for i in RUNTIME_ERROR:
        output.write(f'error_message_{i} db "{RUNTIME_ERROR[i]}", 10, 0\n')
    for i, var in enumerate(var_struct):
        if var_struct[var]['type']==OPU8 and var_struct[var]['value']!= None:
            output.write(f"{var} db {var_struct[var]['value']}\n")
        elif var_struct[var]['type']==OPU16 and var_struct[var]['value']!= None:
            output.write(f"{var} dw {var_struct[var]['value']}\n")
        elif var_struct[var]['type']==OPU32 and var_struct[var]['value']!= None:
            output.write(f"{var} dd {var_struct[var]['value']}\n")
        elif var_struct[var]['type']==OPU64 and var_struct[var]['value']!= None:
            output.write(f"{var} dq {var_struct[var]['value']}\n")   
        else:
            bss_var.append(var)     
    output.write(BSS)
    for var in bss_var:
        if var_struct[var]['type']==OPU8:
            output.write(f"{var}: resb 1\n")
        elif var_struct[var]['type']==OPU16:
            output.write(f"{var}: resw 2\n")
        elif var_struct[var]['type']==OPU32:
            output.write(f"{var}: resd 4\n")
        elif var_struct[var]['type']==OPU64:
            output.write(f"{var}: resq 8\n")
    output.close()
    if libc:
        os.system(f"nasm -felf64 {asmfile}  &&  gcc -static {outfile}.o -o {outfile} ")
    else:
        os.system(f"nasm -felf64 {asmfile}  &&  ld -static {outfile}.o -o {outfile} ")
    return error