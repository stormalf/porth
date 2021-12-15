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
def simulate(program: List, parameter: List, outfile:str) -> Tuple[List,bool, int]:
    global exit_code, runtime_error_counter, MAX_LOOP_SECURITY, var_struct
    conditions_stack = {}
    assert get_OPS() == get_MAX_OPS(),  "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())  
    stack=[]
    error = False
    #isMem = False
    ip = 0
    str_size= NULL_POINTER_PADDING
    #stack.append(0)
    mem = bytearray(NULL_POINTER_PADDING +  get_STR_CAPACITY() +  get_ARGV_CAPACITY() + get_MEM_CAPACITY())
    outlist=[outfile]
    parameter.insert(0, outlist)
    argv_buf_ptr = NULL_POINTER_PADDING + get_STR_CAPACITY()
    str_buf_ptr  = NULL_POINTER_PADDING
    mem_buf_ptr  = NULL_POINTER_PADDING + get_STR_CAPACITY() + get_ARGV_CAPACITY()
    argc = 0
    #stack.append(0)
    for arg in parameter:        
        value = arg[0].encode('utf-8')
        n = len(value)
        arg_ptr = str_buf_ptr + str_size
        mem[arg_ptr:arg_ptr+n] = value
        mem[arg_ptr+n] = 0
        #stack.append(arg_ptr)
        str_size += n + 1  # +1 for the null byte
        assert str_size <= get_STR_CAPACITY(), "string buffer overflow!"
        argv_ptr = argv_buf_ptr+argc*8
        mem[argv_ptr:argv_ptr+8] = arg_ptr.to_bytes(8, byteorder='little')
        argc += 1
        assert argc*8 <= get_ARGV_CAPACITY(), "argv buffer overflow!"
    stack.append(argc)
    #print(mem[argv_buf_ptr:10])    
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
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)
                    stack.append(a_value + b_value)
            elif op['type']==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(a_value - b_value)
            elif op['type']==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                
                    stack.append(int(a_value == b_value)) 
            elif op['type']==get_OP_DUMP():
                if len(stack) == 0:
                    runtime_error_counter += 1                    
                    print("stack is empty impossible to dump")
                    error = True
                else:
                    a = stack.pop()
                    if program[ip - 1]['type'] == get_OP_IDVAR():
                        print(var_struct[a]['value'])
                    else:
                        print(a)
                ip += 1   
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
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    stack.append(a_value)
                    stack.append(a_value)
                ip += 1 
                #print(stack)
            elif op['type']==get_OP_DUP2():
                if len(stack) < 2:
                    print("2DUP impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)               
                    stack.append(a_value)
                    stack.append(b_value)
                    stack.append(a_value)
                    stack.append(b_value)
                ip += 1                 
            elif op['type']==get_OP_GT():
                if len(stack) < 2:
                    print("> impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(int(a_value > b_value)) 
                ip += 1        
            elif op['type']==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(int(a_value < b_value))                 
                ip += 1   
            elif op['type']==get_OP_GE():                
                if len(stack) < 2:
                    print(">= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                   
                    stack.append(int(a_value >= b_value))                 
                ip += 1
            elif op['type']==get_OP_LE():
                if len(stack) < 2:
                    print("<= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(int(a_value <= b_value))                 
                ip += 1
            elif op['type']==get_OP_NE():
                if len(stack) < 2:
                    print("!= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                   
                    stack.append(int(a_value != b_value))                 
                ip += 1
            elif op['type']==get_OP_DIV():
                if len(stack) < 2:
                    print("/ impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)
                    else:
                        stack.append(int(a_value / b_value))                 
                ip += 1
            elif op['type']==get_OP_DIVMOD():
                if len(stack) < 2:
                    print("DIVMOD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)
                    else:
                        stack.append(int(a_value % b_value)) 
                        stack.append(int(a_value / b_value))   
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
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(int(a_value * b_value))                 
                ip += 1
            elif op['type']==get_OP_WHILE():
                ip += 1                
            elif op['type']==get_OP_DO():
                a = stack.pop()
                level = op['level']
                if level not in conditions_stack:
                    conditions_stack[level] = MAX_LOOP_SECURITY
                else:
                    loop_security = conditions_stack[level]
                    loop_security -= 1
                    conditions_stack[level] = loop_security
                if conditions_stack[level] == 0:
                    print(RUNTIME_ERROR[RUN_INFINITE_LOOP])
                    runtime_error_counter += 1
                    error = True
                    sys.exit(RUN_INFINITE_LOOP)
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
                stack.append(mem_buf_ptr)
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
            elif op['type']==get_OP_LOAD64():
                # addr = stack.pop()
                # byte = mem[addr]
                # stack.append(byte)
                addr = stack.pop()
                _bytes = bytearray(8)
                for offset in range(0,8):
                    _bytes[offset] = mem[addr + offset]
                stack.append(int.from_bytes(_bytes, byteorder="little"))

                ip += 1
            elif op['type']==get_OP_STORE64():
                #print(stack)
                store_value64 = stack.pop().to_bytes(length=8, byteorder="little")
                store_addr64 = stack.pop()
                for byte in store_value64:
                    mem[store_addr64] = byte
                    store_addr64 += 1
                ip += 1
            elif op['type']==get_OP_SWAP():
                if len(stack) < 2:
                    print("SWAP impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    a = stack.pop()
                    b = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value)
                    stack.append(b_value)
                ip += 1        
            elif op['type']==get_OP_SHL():
                if len(stack) < 2:
                    print("SHL impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value << b_value)
                ip += 1      
            elif op['type']==get_OP_SHR():
                if len(stack) < 2:
                    print("SHR impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value >> b_value)
                ip += 1
            elif op['type']==get_OP_ORB():
                if len(stack) < 2:
                    print("ORB impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value | b_value)
                ip += 1
            elif op['type']==get_OP_ANDB():
                if len(stack) < 2:
                    print("ANDB impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value & b_value)
                ip += 1         
            elif op['type']==get_OP_DROP():
                stack.pop()
                ip += 1
            elif op['type']==get_OP_OVER():
                b = stack.pop()
                a = stack.pop()
                a_value = get_var_value(a)
                b_value = get_var_value(b)                
                stack.append(a_value)
                stack.append(b_value)
                stack.append(a_value)
                ip += 1
            elif op['type']==get_OP_MOD():
                if len(stack) < 2:
                    print("MOD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)                        
                    else:
                        stack.append(a_value % b_value)
                ip += 1
            elif op['type']==get_OP_EXIT():
                syscall_number = 60
                a = stack.pop()
                exit_code = get_var_value(a)
                break
            elif op['type']==get_OP_WRITE():
                if program[ip-1]['type']==get_OP_CHAR():
                    print(chr(program[ip - 1]['value']), end="")
                elif len(stack) < 2:
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
                stack.append(exit_code)          
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
                stack.append(exit_code)                    
                ip += 1 
            elif op['type']==get_OP_SYSCALL2():
                print("not implemented yet!")
                runtime_error_counter += 1
                error = True    
                stack.append(exit_code)              
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
                        runtime_error_counter += 1
                        error = True
                    stack.append(exit_code) 
                elif syscall_number == 0:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    if fd == 0:
                        s = sys.stdin.readline()
                        #print(s, len(s))
                        mem[buffer:buffer+len(s)] = s.encode('utf-8')
                        buffer += len(s)
                        stack.append(len(s))
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
                stack.append(exit_code)              
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL5():
                print("not implemented yet!")
                error = True                
                stack.append(exit_code)              
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL6():
                print("not implemented yet!")
                error = True                
                stack.append(exit_code)              
                ip += 1  
            elif op['type']==get_OP_CHAR():
                stack.append(op['value'])
                ip += 1
            elif op['type']==get_OP_STRING():
                bstr = bytes(op['value'], 'utf-8')
                strlen = len(bstr)
                stack.append(strlen)
                if 'addr' not in op:
                    str_ptr = str_buf_ptr+str_size
                    op['addr'] = str_ptr
                    mem[str_ptr:str_ptr+strlen] = bstr
                    str_size += strlen
                    assert str_size <= get_STR_CAPACITY(), "String buffer overflow!"
                stack.append(op['addr'])
                # str_ptr = str_buf_ptr+str_size
                # str_ptrs[ip] = str_ptr
                # mem[str_ptr:str_ptr+n] = value
                # str_size += n
                # assert str_size <= STR_CAPACITY, "String buffer overflow"
                # stack.append(str_ptrs[ip])

                ip += 1
            elif op['type']==get_OP_VAR():
                ip += 1
            elif op['type']==get_OP_IDVAR():
                stack.append(op['value'])
                ip += 1
            elif op['type']==get_OP_ARGC():
                stack.append(argc)
                ip += 1
            elif op['type']==get_OP_ARGV():
                stack.append(argv_buf_ptr)
                ip += 1

            elif op['type']==get_OP_ASSIGN_VAR():
                if len(stack) < 1:
                    print("! impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    a = stack.pop()
                    a_value = get_var_value(a)
                    var = op['value'][1:]
                    var_struct[var]['value'] = a_value
                    #print(var_struct[var])
                    stack.append(var_struct[var]['value']) 
                ip += 1                                         
            elif op['type']==get_OP_VARTYPE():              
                ip += 1
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
        # if isMem:
        #     print()
        #     print(f"memory dump {mem[:20]}")  
    # print("----------------------------------")  
    # print(stack)
    # print("----------------------------------")  
    return stack, error, exit_code  

# program = [{'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Test\n', 'loc': ('./tests/macro1.porth', 7, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 7, 10), 'value': 'WRITE', 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 11, 1), 'value': 13, 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 15, 1), 'value': 12, 'jmp': None}, {'type': 12, 'loc': ('./tests/macro1.porth', 19, 7), 'value': '<', 'jmp': None}, {'type': 5, 'loc': ('./tests/macro1.porth', 19, 9), 'value': 'IF', 'jmp': None}, {'type': 41, 'value': 'test2 number 1  < number 2\n', 'loc': ('./tests/macro1.porth', 20, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 20, 32), 'value': 'WRITE', 'jmp': None}, {'type': 7, 'loc': ('./tests/macro1.porth', 21, 1), 'value': 'ELSE', 'jmp': None}, {'type': 41, 'value': 'test2 number 1 >= number 2\n', 'loc': ('./tests/macro1.porth', 22, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 22, 32), 'value': 'WRITE', 'jmp': None}, {'type': 6, 'loc': ('./tests/macro1.porth', 23, 1), 'value': 'END', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}]
# print(len(program))
# simulate(program)