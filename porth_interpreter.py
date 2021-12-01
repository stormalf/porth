#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from typing import Tuple
from porth_globals import *
from typing import *

runtime_error_counter = 0

def get_runtime_error() -> int:
    global runtime_error_counter
    return runtime_error_counter

#simulate the program execution without compiling it
def simulate(program: List) -> Tuple[List,bool, int]:
    global exit_code, runtime_error_counter
    assert get_OPS() == get_MAX_OPS(),  "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())  
    stack=[]
    error = False
    isMem = False
    ip = 0
    str_size= 0
    mem = bytearray( get_STR_CAPACITY() + get_MEM_CAPACITY())
    if not error:
        while ip < len(program):
            op = program[ip]
            if op['type']==get_OP_PUSH():
                ip += 1
                stack.append(op['value'])
            elif op['type']==get_OP_ADD():
                ip += 1                
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
            elif op['type']==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
            elif op['type']==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(int(b == a)) 
            elif op['type']==get_OP_DUMP():
                ip += 1                
                if len(stack) == 0:
                    runtime_error_counter += 1                    
                    print("stack is empty impossible to dump")
                    error = True
                else:
                    a = stack.pop()
                    print(a)
            elif op['type']==get_OP_IF():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to execute if statement")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    a = stack.pop()
                    if a == 0:
                        if len(op) >= 2:
                            ip = op['jmp']
                        else:
                            print("if statement without jmp")
                            runtime_error_counter += 1                    
                            error = True
            elif op['type']==get_OP_ELSE():
                if len(op) >= 2:
                    ip = op['jmp']
                else:
                    print("else statement without jmp")
                    runtime_error_counter += 1                    
                    error = True
            elif op['type']==get_OP_END():
                if len(op) >= 2:
                    ip = op['jmp']
                else:
                    print("end statement without jmp")
                    runtime_error_counter += 1                    
                    error = True
            elif op['type']==get_OP_DUP():
                if len(stack) == 0:
                    print("stack is empty impossible to duplicate")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    a = stack.pop()
                    stack.append(a)
                    stack.append(a)
                ip += 1 
            elif op['type']==get_OP_DUP2():
                if len(stack) < 2:
                    print("2DUP impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
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
                    runtime_error_counter += 1
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a > b)) 
                ip += 1        
            elif op['type']==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a < b))                 
                ip += 1   
            elif op['type']==get_OP_GE():                
                if len(stack) < 2:
                    print(">= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a >= b))                 
                ip += 1
            elif op['type']==get_OP_LE():
                if len(stack) < 2:
                    print("<= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a <= b))                 
                ip += 1
            elif op['type']==get_OP_NE():
                if len(stack) < 2:
                    print("!= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(a != b))                 
                ip += 1
            elif op['type']==get_OP_DIV():
                if len(stack) < 2:
                    print("/ impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if b == 0:
                        print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)
                    else:
                        stack.append(int(a / b))                 
                ip += 1
            elif op['type']==get_OP_MUL():
                if len(stack) < 2:
                    print("MUL impossible not enough element in stack")
                    runtime_error_counter += 1
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
                    if len(op) >= 2:
                        ip = op['jmp']
                    else:
                        print("do statement without jmp")
                        runtime_error_counter += 1                    
                        error = True
                else:
                    ip += 1    
            elif op['type']==get_OP_MEM():
                isMem = True
                stack.append(STR_CAPACITY)
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
                if len(stack) < 2:
                    print("SWAP impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a)
                    stack.append(b)
                ip += 1        
            elif op['type']==get_OP_SHL():
                if len(stack) < 2:
                    print("SHL impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a << b)
                ip += 1      
            elif op['type']==get_OP_SHR():
                if len(stack) < 2:
                    print("SHR impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a >> b)
                ip += 1
            elif op['type']==get_OP_ORB():
                if len(stack) < 2:
                    print("ORB impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a | b)
                ip += 1
            elif op['type']==get_OP_ANDB():
                if len(stack) < 2:
                    print("ANDB impossible not enough element in stack")
                    runtime_error_counter += 1
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
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if b == 0:
                        print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)                        
                    else:
                        stack.append(a % b)
                ip += 1
            elif op['type']==get_OP_EXIT():
                syscall_number = 60
                exit_code = stack.pop()
                break
            elif op['type']==get_OP_WRITE():
                if len(stack) < 2:
                    print("WRITE impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop() #addr
                    a = stack.pop() #length
                    offset = (b+a) 
                    s = mem[b:offset].decode('utf-8')
                    print(s, end='')
                ip += 1
            elif op['type']==get_OP_SYSCALL0():
                syscall_number = stack.pop()
                if syscall_number == 39:
                    stack.append(os.getpid())
                else:
                    print(f"unknown syscall0 number: {syscall_number}")
                    runtime_error_counter += 1
                    error = True                
                ip += 1
            elif op['type']==get_OP_SYSCALL1():
                syscall_number = stack.pop()
                exit_code = stack.pop()
                if syscall_number == 60:
                    break
                else:
                    print(f"unknown syscall1: {syscall_number}")
                    runtime_error_counter += 1
                    error = True                
                ip += 1 
            elif op['type']==get_OP_SYSCALL2():
                print("not implemented yet!")
                runtime_error_counter += 1
                error = True                
                ip += 1                     
            elif op['type']==get_OP_SYSCALL3():
                #print(stack)
                syscall_number = stack.pop()
                arg1 = stack.pop()
                arg2 = stack.pop()
                arg3 = stack.pop()
                #print(f"syscall3: {syscall_number} {arg1} {arg2} {arg3}")
                if syscall_number == 1:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    s = mem[buffer:buffer+count].decode('utf-8')
                    #print(s, buffer, buffer+count)
                    if fd == 1:
                        print(s, end='')
                    elif fd == 2:
                        print(s, end='', file=sys.stderr)
                    else:
                        print(f"unknown file descriptor: {fd}")
                        runtime_error_counter += 1
                        error = True
                else:
                    print(f"unknown syscall3: {syscall_number}")
                    runtime_error_counter += 1
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
            elif op['type']==get_OP_STRING():
                #n = len(op['value'])
                bstr = bytes(op['value'], 'utf-8')
                strlen = len(bstr)
                stack.append(strlen)
                if 'addr' not in op:
                    op['addr'] = str_size
                    mem[str_size:str_size+strlen] = bstr
                    str_size += strlen
                    assert str_size <= get_STR_CAPACITY(), "String buffer overflow!"
                stack.append(op['addr'])
                #print(stack)
                ip += 1
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
        # if isMem:
        #     print()
        #     print(f"memory dump {mem[:20]}")  
    #print("----------------------------------")  
    return stack, error, exit_code  

# program = [{'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Test\n', 'loc': ('./tests/macro1.porth', 7, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 7, 10), 'value': 'WRITE', 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 11, 1), 'value': 13, 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 15, 1), 'value': 12, 'jmp': None}, {'type': 12, 'loc': ('./tests/macro1.porth', 19, 7), 'value': '<', 'jmp': None}, {'type': 5, 'loc': ('./tests/macro1.porth', 19, 9), 'value': 'IF', 'jmp': None}, {'type': 41, 'value': 'test2 number 1  < number 2\n', 'loc': ('./tests/macro1.porth', 20, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 20, 32), 'value': 'WRITE', 'jmp': None}, {'type': 7, 'loc': ('./tests/macro1.porth', 21, 1), 'value': 'ELSE', 'jmp': None}, {'type': 41, 'value': 'test2 number 1 >= number 2\n', 'loc': ('./tests/macro1.porth', 22, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 22, 32), 'value': 'WRITE', 'jmp': None}, {'type': 6, 'loc': ('./tests/macro1.porth', 23, 1), 'value': 'END', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}]
# print(len(program))
# simulate(program)