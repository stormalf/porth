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
push 34
push 35
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
push 70
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_8 
push 420
pop rax 
call print
; end 
addr_8: 
push 34
push 35
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
push 69
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_17 
push 777
pop rax 
call print
; end 
addr_17: 
push 17
pop rax 
call print
push 12
push 12
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
push 24
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_29 
push 24
pop rax 
call print
; else 
jmp    addr_31 
addr_29: 
push 2
pop rax 
call print
; end 
addr_31: 
push 10
push 10
; sub 
pop    rbx 
pop    rax 
sub    rax, rbx 
push    rax 
push 0
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
; if 
pop    rax 
test    rax, rax 
jz    addr_51 
push 1
; if 
pop    rax 
test    rax, rax 
jz    addr_43 
push 10
pop rax 
call print
; else 
jmp    addr_45 
addr_43: 
push 20
pop rax 
call print
; end 
addr_45: 
push 19
pop rax 
call print
