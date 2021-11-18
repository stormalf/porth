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
push 420
addr_1: 
; push 
push 421
addr_2: 
; gt 
mov    rcx, 0 
mov    rdx, 1 
pop    rbx 
pop    rax 
cmp    rax, rbx 
cmovg  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_3: 
; if 
pop    rax 
test    rax, rax 
jz    addr_7 
addr_4: 
; push 
push 1
addr_5: 
pop rax 
call print
addr_6: 
; else 
jmp    addr_9 
addr_7: 
addr_7: 
; push 
push 0
addr_8: 
pop rax 
call print
addr_9: 
; end 
addr_10: 
; push 
push 420
addr_11: 
; push 
push 421
addr_12: 
; lt 
mov    rcx, 0 
mov    rdx, 1 
pop    rbx 
pop    rax 
cmp    rax, rbx 
cmovl  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_13: 
; if 
pop    rax 
test    rax, rax 
jz    addr_17 
addr_14: 
; push 
push 1
addr_15: 
pop rax 
call print
addr_16: 
; else 
jmp    addr_19 
addr_17: 
addr_17: 
; push 
push 0
addr_18: 
pop rax 
call print
addr_19: 
; end 
addr_20: 
; push 
push 10
addr_21: 
; dup 
pop rax 
push rax
push rax
addr_22: 
pop rax 
call print
addr_23: 
pop rax 
call print
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
