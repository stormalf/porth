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
push 70
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
push 69
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
addr_18: 
; push 
push 17
addr_19: 
pop rax 
call print
addr_20: 
; push 
push 12
addr_21: 
; push 
push 12
addr_22: 
; add 
pop    rax 
pop    rbx 
add    rax, rbx 
push    rax 
addr_23: 
; push 
push 24
addr_24: 
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_25: 
; if 
pop    rax 
test    rax, rax 
jz    addr_29 
addr_26: 
; push 
push 24
addr_27: 
pop rax 
call print
addr_28: 
; else 
jmp    addr_31 
addr_29: 
addr_29: 
; push 
push 2
addr_30: 
pop rax 
call print
addr_31: 
; end 
addr_32: 
; push 
push 10
addr_33: 
; push 
push 10
addr_34: 
; sub 
pop    rbx 
pop    rax 
sub    rax, rbx 
push    rax 
addr_35: 
; push 
push 0
addr_36: 
; equal 
mov    rcx, 0 
mov    rdx, 1 
pop    rax 
pop    rbx 
cmp    rax, rbx 
cmove  rcx, rdx 
mov  rax, rcx 
push    rax 
addr_37: 
; if 
pop    rax 
test    rax, rax 
jz    addr_48 
addr_38: 
; push 
push 1
addr_39: 
; if 
pop    rax 
test    rax, rax 
jz    addr_43 
addr_40: 
; push 
push 10
addr_41: 
pop rax 
call print
addr_42: 
; else 
jmp    addr_45 
addr_43: 
addr_43: 
; push 
push 20
addr_44: 
pop rax 
call print
addr_45: 
; end 
addr_46: 
; push 
push 19
addr_47: 
pop rax 
call print
addr_48: 
; end 
mov rax, SYS_EXIT
mov rdi, 69
syscall
section .data
format db  "%d", 10, 0
