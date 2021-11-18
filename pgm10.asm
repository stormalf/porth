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
push 100
addr_1: 
; while 
addr_2: 
; dup 
pop rax 
push rax
push rax
addr_3: 
; push 
push 0
addr_4: 
; gt 
mov    rcx, 0 
mov    rdx, 1 
pop    rbx 
pop    rax 
cmp    rax, rbx 
cmovg  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_5: 
; do 
pop    rax 
test    rax, rax 
jz    addr_11 
addr_6: 
; dup 
pop rax 
push rax
push rax
addr_7: 
pop rax 
call print
addr_8: 
; push 
push 1
addr_9: 
; sub 
pop    rbx 
pop    rax 
sub    rax, rbx 
push    rax 
addr_10: 
; end 
jmp    addr_1 
addr_11: 
; push 
push 100
addr_12: 
pop rax 
call print
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
