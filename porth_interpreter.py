#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from porth_lexer import get_OP_ADD, get_OP_SUB, get_OP_PUSH, get_OP_DUMP, get_OP_SWAP, get_MAX_OPS, \
    get_OP_EQUAL, get_OPS, get_OP_IF, get_OP_END, get_OP_ELSE, get_OP_DUP, get_OP_DUP2, get_MEM_CAPACITY, \
    get_OP_GT, get_OP_LT, get_OP_WHILE, get_OP_DO, get_OP_MEM, get_OP_LOAD, get_OP_STORE, get_OP_RETURN, \
    get_OP_SYSCALL1, get_OP_SYSCALL2, get_OP_SYSCALL3, get_OP_SYSCALL4, get_OP_SYSCALL5, get_OP_SYSCALL6, \
    get_OP_DROP, get_OP_SHL, get_OP_SHR, get_OP_ORB, get_OP_ANDB, get_OP_OVER, get_OP_MOD, \
    get_OP_GE, get_OP_LE, get_OP_NE, get_OP_DIV, get_OP_MUL, exit_code



#simulate the program execution without compiling it
def simulate(program):
    global exit_code
    assert get_OPS() == get_MAX_OPS(),  "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())  
    stack=[]
    error = False
    isMem = False
    ip = 0
    #exit_code = 0
    mem = bytearray(get_MEM_CAPACITY())
    #print(program)
    if not error:
        while ip < len(program):
            #print(stack)
            op = program[ip]
            if op['type']==get_OP_PUSH():
                ip += 1
                stack.append(op['value'])
            elif op['type']==get_OP_ADD():
                ip += 1                
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op['type']==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op['type']==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a)) 
            elif op['type']==get_OP_DUMP():
                ip += 1                
                if len(stack) == 0:
                    # print("stack is empty impossible to dump")
                    # error = True
                    pass
                else:
                    a = stack.pop()
                    print(a)
            elif op['type']==get_OP_IF():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to execute if statement")
                    error = True
                else:
                    a = stack.pop()
                    if a == 0:
                        assert len(op) >= 2, "if instruction does not have an End instruction!"
                        ip = op['jmp']
                        pass
            elif op['type']==get_OP_ELSE():
                #ip += 1  
                assert len(op) >= 2, "else instruction does not have an End instruction!"   
                ip = op['jmp']                      
            elif op['type']==get_OP_END():
                assert len(op) >= 2, "end instruction does not have next instruction to jump check the crossreferences!"                 
                ip = op['jmp']
            elif op['type']==get_OP_DUP():
                a = stack.pop()
                stack.append(a)
                stack.append(a)
                ip += 1 
            elif op['type']==get_OP_DUP2():
                b = stack.pop()
                a = stack.pop()
                stack.append(a)
                stack.append(b)
                stack.append(a)
                stack.append(b)                
                ip += 1                 
            elif op['type']==get_OP_GT():
                if len(stack) < 2:
                    print("> impossible not enough element in stack")
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a > b)) 
                ip += 1        
            elif op['type']==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a < b))                 
                ip += 1   
            elif op['type']==get_OP_GE():                
                if len(stack) < 2:
                    print(">= impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a >= b))                 
                ip += 1
            elif op['type']==get_OP_LE():
                if len(stack) < 2:
                    print("<= impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a <= b))                 
                ip += 1
            elif op['type']==get_OP_NE():
                if len(stack) < 2:
                    print("!= impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a != b))                 
                ip += 1
            elif op['type']==get_OP_DIV():
                if len(stack) < 2:
                    print("/ impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if b == 0:
                        print("DIV by zero")
                        error = True
                    else:
                        stack.append(int(a / b))                 
                ip += 1
            elif op['type']==get_OP_MUL():
                if len(stack) < 2:
                    print("MUL impossible not enough element in stack")
                    error = True
                else:
                    #print(stack)
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a * b))                 
                ip += 1
            elif op['type']==get_OP_WHILE():
                ip += 1                
            elif op['type']==get_OP_DO():
                #ip += 1
                a = stack.pop()
                if a == 0:
                    assert len(op) >= 2, "end instruction does not have next instruction to jump, check the crossreferences!"    
                    ip = op['jmp']
                else:
                    ip += 1    
            elif op['type']==get_OP_MEM():
                isMem = True
                stack.append(0)
                ip += 1   
            elif op['type']==get_OP_LOAD():
                addr = stack.pop()
                byte = mem[addr]
                stack.append(byte)
                ip += 1                    
            elif op['type']==get_OP_STORE():
                value = stack.pop()
                addr = stack.pop()
                mem[addr] = value & 0xFF
                ip += 1   
            elif op['type']==get_OP_SWAP():
                a = stack.pop()
                b = stack.pop()
                stack.append(a)
                stack.append(b)
                ip += 1        
            elif op['type']==get_OP_SHL():
                if len(stack) < 2:
                    print("SHL impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a << b)
                ip += 1      
            elif op['type']==get_OP_SHR():
                if len(stack) < 2:
                    print("SHR impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a >> b)
                ip += 1
            elif op['type']==get_OP_ORB():
                if len(stack) < 2:
                    print("ORB impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a | b)
                ip += 1
            elif op['type']==get_OP_ANDB():
                if len(stack) < 2:
                    print("ANDB impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a & b)
                ip += 1         
            elif op['type']==get_OP_DROP():
                stack.pop()
                ip += 1
            elif op['type']==get_OP_OVER():
                a = stack.pop()
                b = stack.pop()
                stack.append(b)
                stack.append(a)
                stack.append(b)
                ip += 1
            elif op['type']==get_OP_MOD():
                if len(stack) < 2:
                    print("MOD impossible not enough element in stack")
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if b == 0:
                        print("MOD by zero")
                        error = True
                    else:
                        stack.append(a % b)
                ip += 1
            elif op['type']==get_OP_RETURN():
                syscall_number = 60
                exit_code = stack.pop()
                break
            elif op['type']==get_OP_SYSCALL1():
                syscall_number = stack.pop()
                exit_code = stack.pop()
                if syscall_number == 60:
                    break
                else:
                    print(f"unknown syscall3: {syscall_number}")
                    error = True                
                ip += 1 
            elif op['type']==get_OP_SYSCALL2():
                print("not implemented yet!")
                error = True                
                ip += 1                     
            elif op['type']==get_OP_SYSCALL3():
                syscall_number = stack.pop()
                arg1 = stack.pop()
                arg2 = stack.pop()
                arg3 = stack.pop()
                if syscall_number == 1:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    s = mem[buffer:buffer+count].decode('utf-8')
                    if fd == 1:
                        print(s, end='')
                    elif fd == 2:
                        print(s, end='', file=sys.stderr)
                    else:
                        print(f"unknown file descriptor: {fd}")
                        error = True
                else:
                    print(f"unknown syscall1: {syscall_number}")
                    error = True
                ip += 1    
            elif op['type']==get_OP_SYSCALL4():
                print("not implemented yet!")
                error = True                
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL5():
                print("not implemented yet!")
                error = True                
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL6():
                print("not implemented yet!")
                error = True                
                ip += 1                                                     
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
        if isMem:
            print(f"memory dump {mem[:20]}")                
    return stack, error, exit_code  
