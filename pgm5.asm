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
push 45
push 45
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
call print
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%20ld", 10, 0
