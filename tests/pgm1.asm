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
push 34
addr_2: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_3: 
pop rax 
call print
addr_4: 
; push 
push 34
addr_5: 
; push 
push 34
addr_6: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_7: 
pop rax 
call print
addr_8: 
; push 
push 500
addr_9: 
; push 
push 80
addr_10: 
; sub 
pop    rbx 
pop    rax 
sub    rax, rbx 
push    rax 
addr_11: 
pop rax 
call print
addr_12: 
; push 
push 344
addr_13: 
; push 
push 75
addr_14: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_15: 
; push 
push 37
addr_16: 
; sub 
pop    rbx 
pop    rax 
sub    rax, rbx 
push    rax 
addr_17: 
pop rax 
call print
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
