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
push 0
; if 
pop    rax 
test    rax, rax 
jz    addr_13 
push 1
; if 
pop    rax 
test    rax, rax 
jz    addr_7 
push 10
pop rax 
call print
; else 
jmp    addr_9 
addr_7: 
push 20
pop rax 
call print
; end 
addr_9: 
push 17
pop rax 
call print
; else 
jmp    addr_15 
addr_13: 
push 40
pop rax 
call print
; end 
addr_15: 
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
