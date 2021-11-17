%define SYS_EXIT 60

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
main:
push 420
push 421
; gt 
mov    rcx, 0 
mov    rdx, 1 
pop    rbx 
pop    rax 
cmp    rax, rbx 
cmovg  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_7 
push 1
pop rax 
call print
; else 
jmp    addr_9 
addr_7: 
push 0
pop rax 
call print
; end 
addr_9: 
push 420
push 421
; lt 
mov    rcx, 0 
mov    rdx, 1 
pop    rbx 
pop    rax 
cmp    rax, rbx 
cmovl  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_17 
push 1
pop rax 
call print
; else 
jmp    addr_19 
addr_17: 
push 0
pop rax 
call print
; end 
addr_19: 
push 10
; dup 
pop rax 
push rax
push rax
pop rax 
call print
pop rax 
call print
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
