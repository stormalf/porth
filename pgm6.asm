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
push 34
addr_1: 
; push 
push 35
addr_2: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_3: 
; push 
push 69
addr_4: 
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_5: 
; if 
pop    rax 
test    rax, rax 
jz    addr_8 
addr_6: 
; push 
push 420
addr_7: 
pop rax 
call print
addr_8: 
; end 
addr_9: 
; push 
push 34
addr_10: 
; push 
push 35
addr_11: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_12: 
; push 
push 70
addr_13: 
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_14: 
; if 
pop    rax 
test    rax, rax 
jz    addr_17 
addr_15: 
; push 
push 777
addr_16: 
pop rax 
call print
addr_17: 
; end 
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
