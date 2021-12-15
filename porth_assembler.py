#!/usr/bin/python3
# -*- coding: utf-8 -*-
from porth_globals import *



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
push_args:
ret
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
FOOTER = f'''
mov rax, SYS_EXIT
mov rdi, 0
syscall
'''

DATA=f'''
section .data 
format db  "%llu", 10, 0
format2 db "%s", 10, 0
char db  "%c", 0
security  dq  {MAX_LOOP_SECURITY}
'''

BSS=f'''
section .bss    ; uninitialized data section
mem: resb {get_MEM_CAPACITY()}
'''



#with libc argc, argv are not passed by the stack but by the registers rdi contains argc and rsi contains argv
#to be able to use the same program with or without libc we need to push the arguments on the stack before executing the porth program
# def generate_read_argv(output):
#         output.write("mov rax, [rsi + (rdi * 8) + 8]\n") 
#         output.write("mov rdx, rdi\n")
#         output.write("check_args:\n")
#         output.write("cmp rdi, 0 \n") 
#         output.write("jz no_args\n")
#         output.write("push rax\n")
#         output.write("mov rax, [rsi + (rdi * 8)]\n")            
#         output.write("dec rdi\n")
#         output.write("jmp check_args\n")
#         output.write("no_args:\n")
#         output.write(f"mov rax, [rsi + 8] \n") 
#         output.write("push rax\n")    
#         output.write(f"mov rax, [rsi] \n")             
#         output.write(f"push rax\n") 
#         output.write(f"push rdx\n")      


def generate_add_op(output):
    output.write("; add \n")
    output.write("pop    rax \n")
    output.write("pop    rcx \n")
    output.write("add    rax, rcx \n")
    output.write("push    rax \n")

def generate_sub_op(output): 
    output.write("; sub \n")
    output.write("pop    rcx \n")
    output.write("pop    rax \n")
    output.write("sub    rax, rcx \n")                
    output.write("push    rax \n")

def generate_equal_op(output):
    output.write("; equal \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    rax \n")
    output.write("pop    r9 \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmove  rcx, rdx \n")  
    output.write("push    rcx \n")   

def generate_dup_op(output):
    output.write("; dup \n")            
    output.write("pop rax \n")
    output.write("push rax\n")               
    output.write("push rax\n") 

def generate_dup2_op(output):
    output.write("; 2dup \n")            
    output.write("pop rcx \n")
    output.write("pop rax \n")            
    output.write("push rax\n")               
    output.write("push rcx\n") 
    output.write("push rax\n")               
    output.write("push rcx\n")  

def generate_gt_op(output):
    output.write("; gt \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    r9 \n")
    output.write("pop    rax \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmovg  rcx, rdx \n")  
    output.write("push    rcx \n") 

def generate_lt_op(output):
    output.write("; lt \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    r9 \n")
    output.write("pop    rax \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmovl  rcx, rdx \n")  
    output.write("push    rcx \n")  

def generate_ge_op(output):
    output.write("; ge \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    r9 \n")
    output.write("pop    rax \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmovge rcx, rdx \n")  
    output.write("push    rcx \n")

def generate_le_op(output):
    output.write("; le \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    r9 \n")
    output.write("pop    rax \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmovle rcx, rdx \n")  
    output.write("push    rcx \n")

def generate_ne_op(output):
    output.write("; ne \n")
    output.write("mov    rcx, 0 \n")
    output.write("mov    rdx, 1 \n")
    output.write("pop    r9 \n")
    output.write("pop    rax \n")            
    output.write("cmp    rax, r9 \n")                
    output.write("cmovne rcx, rdx \n")  
    output.write("push    rcx \n")

def generate_mul_op(output):
    output.write("; mul \n")
    output.write("pop    rcx \n")
    output.write("pop    rax \n")
    output.write("imul   rcx \n")
    output.write("push    rax \n")    

def generate_load_op(output):
    output.write("; load \n")
    output.write("pop rax\n")    
    output.write("xor rbx, rbx\n")           
    output.write("mov bl, [rax]\n")
    output.write("push rbx\n")    

def generate_store_op(output):
    output.write("; store \n")
    output.write("pop rbx\n")
    output.write("pop rax\n")
    output.write("mov [rax], bl\n")    

def generate_load64_op(output):
    output.write("; load64 \n")
    output.write("pop rax\n")
    output.write("xor rcx, rcx\n")
    output.write("mov rcx, [rax]\n")
    output.write("push rcx\n")    

def generate_store64_op(output):
    output.write("; store64 \n")
    output.write("pop rcx\n")
    output.write("pop rax\n")
    output.write("mov [rax], rcx\n")

def generate_swap_op(output):
    output.write("; swap \n") 
    output.write("pop rax\n")
    output.write("pop rcx\n")
    output.write("push rax\n")
    output.write("push rcx\n")    

def generate_shl_op(output):
    output.write("; shl \n")
    output.write("pop rcx\n")
    output.write("pop rax\n")
    output.write("shl rax, cl\n")
    output.write("push rax\n")

def generate_shr_op(output):
    output.write("; shr \n")
    output.write("pop rcx\n")
    output.write("pop rax\n")
    output.write("shr rax, cl\n")
    output.write("push rax\n")

def generate_orb_op(output):
    output.write("; orb \n")
    output.write("pop rcx\n")
    output.write("pop rax\n")
    output.write("or rax, rcx\n")
    output.write("push rax\n")

def generate_andb_op(output):
    output.write("; andb \n")
    output.write("pop rcx\n")
    output.write("pop rax\n")
    output.write("and rax, rcx\n")
    output.write("push rax\n")

def generate_over_op(output):
    output.write("; over \n")
    output.write("pop rax\n")
    output.write("pop rcx\n")
    output.write("push rcx\n")
    output.write("push rax\n")
    output.write("push rcx\n")

def generate_syscall0_op(output):
    output.write("; syscall0 \n")
    output.write("pop rax\n")
    output.write("syscall\n")
    output.write("push rax\n")

def generate_syscall1_op(output):
    output.write("; syscall1 \n")
    output.write("pop rax\n")
    output.write("pop rdi\n")            
    output.write("syscall\n") 
    output.write("push rax\n")

def generate_syscall2_op(output):
    output.write("; syscall2 \n")
    output.write("pop rax\n")
    output.write("pop rdi\n")
    output.write("pop rsi\n")
    output.write("syscall\n")
    output.write("push rax\n")

def generate_syscall3_op(output):
    output.write("; syscall3 \n")
    output.write("pop rax\n")
    output.write("pop rdi\n")            
    output.write("pop rsi\n")
    output.write("pop rdx\n")            
    output.write("syscall\n")
    output.write("push rax\n")

def generate_syscall4_op(output):
    output.write("; syscall4 \n")
    output.write("pop rax\n")
    output.write("pop rdi\n")
    output.write("pop rsi\n")
    output.write("pop rdx\n")
    output.write("pop r10\n")
    output.write("syscall\n")
    output.write("push rax\n")

def generate_syscall5_op(output):    
    output.write("; syscall5 \n")
    output.write("pop rax\n")
    output.write("pop rdi\n")
    output.write("pop rsi\n")
    output.write("pop rdx\n")
    output.write("pop r10\n")
    output.write("pop r8\n")
    output.write("syscall\n")
    output.write("push rax\n")

def generate_syscall6_op(output):
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


def generate_argc_op(output):
    output.write("; argc \n")
    output.write("mov rax, [args_ptr]\n")
    output.write("mov rax, [rax]\n")
    output.write("push rax\n")

def generate_argv_op(output):
    output.write("; argv \n")
    output.write("mov rax, [args_ptr]\n")
    output.write("add rax, 8\n")
    output.write("push rax\n")

#libc argv in rsi
def generate_argv_libc_op(output):
    output.write("; argv \n")
    output.write("mov rax, [args_ptr]\n")
    output.write("push rax\n")    

#libc argc in rdi
def generate_argc_libc_op(output):
    output.write("; argc \n")
    output.write("mov rax, rdi\n")
    output.write("push rax\n")
    output.write("dec rdi\n")    

def generate_push_op(output, value):
    output.write("; push \n")   
    output.write("xor rax, rax\n")
    output.write(f"mov rax, {value}\n")                      
    output.write("push rax\n")

def generate_if_op(output, op):
    assert len(op) >= 2, f"compile error! IF instruction does not have an END instruction! {op}"            
    output.write("; if \n")
    output.write("pop    rax \n")
    output.write("test    rax, rax \n")
    output.write(f"jz    addr_{op['jmp']} \n")    

def generate_else_op(output, op):
    assert len(op) >= 2, f"compile error! ELSE instruction does not have an END instruction! {op}"            
    output.write("; else \n")
    output.write(f"jmp    addr_{op['jmp']} \n")

def generate_end_op(output, op, ip):
    output.write("; end \n")
    assert len(op) >= 2, f"compile error! END instruction does not have a next instruction to jump! {op}"  
    if ip + 1 != op['jmp']:
        output.write(f"jmp    addr_{op['jmp']} \n")       

def generate_dump_op(output, op, libc):
    output.write("; dump \n")
    if libc:
        output.write("pop rax \n")
    else:
        output.write("pop rdi \n")
    output.write("call print\n")   

def generate_div_op(output, ip, libc):
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
    #output.write(f"pop rbp\n")
    output.write("mov rax, SYS_EXIT\n")
    output.write(f"mov rdi, {RUN_DIV_ZERO}\n")            
    output.write("syscall\n")  
    output.write(f"addr_div_end_{ip}:\n")  

def generate_divmod_op(output, ip, libc):
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

def generate_do_op(output, op):
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

def generate_mod_op(output, ip, libc):
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

def generate_exit_op(output):
    output.write("; exit \n")
    output.write("mov rax, SYS_EXIT\n")
    output.write("pop rdi\n")            
    output.write("syscall\n") 

def generate_write_op(output, bytecode_prev_ip, libc):
    if bytecode_prev_ip['type']==get_OP_CHAR():
        output.write("; write char \n")
        if libc:
            output.write(f"mov rax, {bytecode_prev_ip['value']}\n")
            output.write("push rax\n")
            output.write("call print_char\n")
        else:
            output.write(f"mov rdi, {bytecode_prev_ip['value']}\n")
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

def generate_string_op(output, strlen, index):
    output.write("; string \n")
    output.write(f"mov rax, {strlen}\n")
    output.write("push rax\n")
    output.write(f"push str_{index}\n")
  
def generate_idvar_op(output, bytecode_prev_ip, op):
    #if it's not the definition of a variable, we push the value
    if bytecode_prev_ip['type'] != get_OP_VAR():
        value = var_struct[op['value']]['value']
        if value != None:
            output.write("; idvar \n")
            type=get_var_type(op['value'])
            qualifier=get_var_qualifier(type)
            register=get_register(type)
            output.write(f"xor rax, rax\n")
            output.write(f"mov {register},  {qualifier} [{op['value']}]\n")
            output.write(f"push rax\n")

def generate_assign_op(output, bytecode_prev_ip, op):
    global var_struct
    if bytecode_prev_ip['type'] != get_OP_VAR():
        #print(op)
        var = op['variable']
        value = var_struct[var]['value']
        if value != None:
            output.write("; idvar \n")
            type=get_var_type(var)
            qualifier=get_var_qualifier(type)
            register=get_register(type)
            output.write(f"pop rax\n")
            output.write(f"mov {qualifier} [{var}], {register}\n")
            output.write(f"push rax\n")  

def generate_infinite_loop_op(output, libc):
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