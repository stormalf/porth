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
addr_0: 
; push 
push 0
addr_1: 
; if 
pop    rax 
test    rax, rax 
jz    addr_13 
addr_2: 
; push 
push 1
addr_3: 
; if 
pop    rax 
test    rax, rax 
jz    addr_7 
addr_4: 
; push 
push 10
addr_5: 
pop rax 
call print
addr_6: 
; else 
jmp    addr_9 
addr_7: 
; push 
push 20
addr_8: 
pop rax 
call print
addr_9: 
; end 
addr_10: 
; push 
push 17
addr_11: 
pop rax 
call print
addr_12: 
; else 
jmp    addr_15 
addr_13: 
; push 
push 40
addr_14: 
pop rax 
call print
addr_15: 
; end 
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
