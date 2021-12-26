#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import FileIO
import sys
import os
from typing import Tuple
from porth_globals import *
from typing import *


runtime_error_counter = 0

def get_runtime_error() -> int:
    global runtime_error_counter
    return runtime_error_counter

#print only if requested
def print_output_simulation(value, file: FileIO = sys.stdout, end: str = None, istoprint: bool = True) -> None:
    if istoprint:
        if end is None:
            print(value, file=file)
        else:
            print(value, end=end, file=file)

#simulate the program execution without compiling it. To be able to re-use the simulate function to detect some warnings and errors
#the output is printed only if the function is requested with istoprint=True (default behaviour)
def simulate(program: List, parameter: List, outfile:str, istoprint=True) -> Tuple[List,bool, int]:
    global exit_code, runtime_error_counter, MAX_LOOP_SECURITY, var_struct, BUFFER_SIZE
    conditions_stack = {}
    assert get_OPS() == get_MAX_OPS(),  "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())  
    stack=[]
    error = False
    #isMem = False
    ip = 0
    str_size= NULL_POINTER_PADDING
    mem = bytearray(NULL_POINTER_PADDING +  get_STR_CAPACITY() +  get_ARGV_CAPACITY() + get_MEM_CAPACITY())
    buffer_file = bytearray(NULL_POINTER_PADDING + BUFFER_SIZE)
    outlist=[outfile]
    parameter.insert(0, outlist)
    argv_buf_ptr = NULL_POINTER_PADDING + get_STR_CAPACITY()
    str_buf_ptr  = NULL_POINTER_PADDING
    buf_file_ptr = NULL_POINTER_PADDING
    mem_buf_ptr  = NULL_POINTER_PADDING + get_STR_CAPACITY() + get_ARGV_CAPACITY()
    argc = 0
    for arg in parameter:        
        value = arg[0].encode('utf-8')
        n = len(value)
        arg_ptr = str_buf_ptr + str_size
        mem[arg_ptr:arg_ptr+n] = value
        mem[arg_ptr+n] = 0
        str_size += n + 1  # +1 for the null byte
        assert str_size <= get_STR_CAPACITY(), "string buffer overflow!"
        argv_ptr = argv_buf_ptr+argc*8
        mem[argv_ptr:argv_ptr+8] = arg_ptr.to_bytes(8, byteorder='little')
        argc += 1
        assert argc*8 <= get_ARGV_CAPACITY(), "argv buffer overflow!"
    #stack.append(argc)
    #set_stack_counter()
    if not error:
        while ip < len(program):
            op = program[ip]
            if op['type']==get_OP_PUSH():
                ip += 1
                stack.append(op['value'])
                set_stack_counter()
            elif op['type']==get_OP_ADD():
                ip += 1                
                if len(stack) < 2:
                    print("ADD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)
                    stack.append(a_value + b_value)
                    set_stack_counter()
            elif op['type']==get_OP_SUB():
                ip += 1                
                if len(stack) < 2:
                    print("SUB impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(a_value - b_value)
                    set_stack_counter()
            elif op['type']==get_OP_EQUAL():
                ip += 1                
                if len(stack) < 2:
                    print("EQUAL impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                
                    stack.append(int(a_value == b_value)) 
                    set_stack_counter()
            elif op['type']==get_OP_DUMP():
                if len(stack) == 0:
                    runtime_error_counter += 1                    
                    print("stack is empty impossible to dump")
                    error = True
                else:
                    a = stack.pop()
                    set_stack_counter(-1)
                    if program[ip - 1]['type'] == get_OP_IDVAR():
                        #print(var_struct[a]['value'])
                        print_output_simulation(var_struct[a]['value'], istoprint=istoprint)
                    else:
                        #print(a)
                        print_output_simulation(a, istoprint=istoprint)
                ip += 1   
            elif op['type']==get_OP_IF():
                ip += 1                
                if len(stack) == 0:
                    print("stack is empty impossible to execute if statement")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    a = stack.pop()
                    a_value = get_var_value(a)
                    set_stack_counter(-1)
                    if a_value == 0:
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
                    set_stack_counter(-1)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    stack.append(a_value)
                    stack.append(a_value)
                    set_stack_counter(2)
                ip += 1 
            elif op['type']==get_OP_DUP2():
                if len(stack) < 2:
                    print("2DUP impossible not enough element in stack")
                    runtime_error_counter += 1                    
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)               
                    stack.append(a_value)
                    stack.append(b_value)
                    stack.append(a_value)
                    stack.append(b_value)
                    set_stack_counter(4)
                ip += 1                 
            elif op['type']==get_OP_GT():
                if len(stack) < 2:
                    print("> impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:                
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(int(a_value > b_value)) 
                    set_stack_counter()
                ip += 1        
            elif op['type']==get_OP_LT():
                if len(stack) < 2:
                    print("< impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                  
                    stack.append(int(a_value < b_value))  
                    set_stack_counter()               
                ip += 1   
            elif op['type']==get_OP_GE():                
                if len(stack) < 2:
                    print(">= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                   
                    stack.append(int(a_value >= b_value)) 
                    set_stack_counter()                
                ip += 1
            elif op['type']==get_OP_LE():
                if len(stack) < 2:
                    print("<= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(int(a_value <= b_value))    
                    set_stack_counter()            
                ip += 1
            elif op['type']==get_OP_NE():
                if len(stack) < 2:
                    print("!= impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    #if variable retrieve the content value 
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                   
                    stack.append(int(a_value != b_value))     
                    set_stack_counter()            
                ip += 1
            elif op['type']==get_OP_DIV():
                if len(stack) < 2:
                    print("/ impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        #print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)
                    else:
                        stack.append(int(a_value / b_value))
                        set_stack_counter()                 
                ip += 1
            elif op['type']==get_OP_DIVMOD():
                if len(stack) < 2:
                    print("DIVMOD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        #print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)
                    else:
                        stack.append(int(a_value % b_value)) 
                        stack.append(int(a_value / b_value))  
                        set_stack_counter(2) 
                ip += 1                
            elif op['type']==get_OP_MUL():
                if len(stack) < 2:
                    print("MUL impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(int(a_value * b_value))
                    set_stack_counter()                 
                ip += 1
            elif op['type']==get_OP_WHILE():
                ip += 1                
            elif op['type']==get_OP_DO():
                a = stack.pop()
                a_value = get_var_value(a)
                set_stack_counter(-1)
                level = op['level']
                if level not in conditions_stack:
                    conditions_stack[level] = MAX_LOOP_SECURITY
                else:
                    loop_security = conditions_stack[level]
                    loop_security -= 1
                    conditions_stack[level] = loop_security
                if conditions_stack[level] == 0:
                    #print(RUNTIME_ERROR[RUN_INFINITE_LOOP])
                    print_output_simulation(RUNTIME_ERROR[RUN_INFINITE_LOOP], istoprint=istoprint)
                    runtime_error_counter += 1
                    error = True
                    sys.exit(RUN_INFINITE_LOOP)
                if a_value == 0:
                    if len(op) >= 2:
                        ip = op['jmp']
                    else:
                        print("do statement without jmp")
                        runtime_error_counter += 1                    
                        error = True
                else:
                    ip += 1    
            elif op['type']==get_OP_MEM():
                #isMem = True
                stack.append(mem_buf_ptr)
                set_stack_counter()
                ip += 1  
            elif op['type']==get_OP_LOAD():
                addr = stack.pop()
                a_value = get_var_value(addr)
                set_stack_counter(-1)
                byte = mem[a_value]
                stack.append(byte)
                set_stack_counter()
                ip += 1                    
            elif op['type']==get_OP_STORE():
                value = stack.pop()
                addr = stack.pop()
                a_value = get_var_value(value)                
                b_value = get_var_value(addr)                                
                set_stack_counter(-2)
                mem[b_value] = a_value & 0xFF
                ip += 1  
            elif op['type']==get_OP_LOAD16():
                a = stack.pop()
                set_stack_counter(-1)
                addr = get_var_value(a)                
                _bytes = bytearray(2)
                for offset in range(0,2):
                    _bytes[offset] = mem[addr + offset]
                stack.append(int.from_bytes(_bytes, byteorder="little"))
                set_stack_counter()
                ip += 1                    
            elif op['type']==get_OP_STORE16():
                a = stack.pop()
                store_value = get_var_value(a)                
                store_value16 = store_value.to_bytes(length=2, byteorder="little",  signed=(store_value < 0))
                b = stack.pop()
                store_addr16 = get_var_value(b)                
                set_stack_counter(-2)
                for byte in store_value16:
                    mem[store_addr16] = byte
                    store_addr16 += 1
                ip += 1                   
            elif op['type']==get_OP_LOAD32():
                a = stack.pop()
                addr = get_var_value(a)      
                set_stack_counter(-1)          
                _bytes = bytearray(4)
                #print(addr, mem[addr:20])                    
                for offset in range(0,4):
                    _bytes[offset] = mem[addr + offset]
                stack.append(int.from_bytes(_bytes, byteorder="little"))
                set_stack_counter()
                ip += 1                     
            elif op['type']==get_OP_STORE32():
                a = stack.pop()
                store_value = get_var_value(a)                
                store_value32 = store_value.to_bytes(length=4, byteorder="little",  signed=(store_value < 0))
                b = stack.pop()
                store_addr32 = get_var_value(b)   
                #print(store_value32, store_addr32, mem[store_addr32:20])                 
                set_stack_counter(-2)
                for byte in store_value32:
                    mem[store_addr32] = byte
                    store_addr32 += 1
                ip += 1                
            elif op['type']==get_OP_LOAD64():
                a = stack.pop()
                addr = get_var_value(a)
                set_stack_counter(-1)
                #print("load64", addr, mem[addr:20])
                _bytes = bytearray(8)
                for offset in range(0,8):
                    _bytes[offset] = mem[addr + offset]
                stack.append(int.from_bytes(_bytes, byteorder="little"))
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_STORE64():
                a = stack.pop()
                store_value = get_var_value(a)                
                store_value64 = store_value.to_bytes(length=8, byteorder="little",  signed=(store_value < 0))
                b = stack.pop()
                store_addr64 = get_var_value(b)                
                #print("store64", store_addr64, mem[0:100])                
                set_stack_counter(-2)
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
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value)
                    stack.append(b_value)
                    set_stack_counter(2)
                ip += 1        
            elif op['type']==get_OP_SHL():
                if len(stack) < 2:
                    print("SHL impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value << b_value)
                    set_stack_counter()
                ip += 1      
            elif op['type']==get_OP_SHR():
                if len(stack) < 2:
                    print("SHR impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value >> b_value)
                    set_stack_counter()
                ip += 1
            elif op['type']==get_OP_ORB():
                if len(stack) < 2:
                    print("ORB impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value | b_value)
                    set_stack_counter()
                ip += 1
            elif op['type']==get_OP_ANDB():
                if len(stack) < 2:
                    print("ANDB impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    stack.append(a_value & b_value)
                    set_stack_counter()
                ip += 1         
            elif op['type']==get_OP_DROP():
                stack.pop()
                set_stack_counter(-1)
                ip += 1
            elif op['type']==get_OP_OVER():
                b = stack.pop()
                a = stack.pop()
                set_stack_counter(-2)
                a_value = get_var_value(a)
                b_value = get_var_value(b)                
                stack.append(a_value)
                stack.append(b_value)
                stack.append(a_value)
                set_stack_counter(3)
                ip += 1
            elif op['type']==get_OP_MOD():
                if len(stack) < 2:
                    print("MOD impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-2)
                    a_value = get_var_value(a)
                    b_value = get_var_value(b)                    
                    if b_value == 0:
                        #print(RUNTIME_ERROR[RUN_DIV_ZERO])
                        print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
                        runtime_error_counter += 1
                        error = True
                        sys.exit(RUN_DIV_ZERO)                        
                    else:
                        stack.append(a_value % b_value)
                        set_stack_counter()
                ip += 1
            elif op['type']==get_OP_EXIT():
                syscall_number = 60
                a = stack.pop()
                set_stack_counter(-1)
                exit_code = get_var_value(a)
                break
            elif op['type']==get_OP_WRITE():
                if program[ip-1]['type']==get_OP_CHAR():
                    #print(chr(program[ip - 1]['value']), end="")
                    print_output_simulation(chr(program[ip - 1]['value']), end="", istoprint=istoprint)
                elif program[ip-1]['type']==get_OP_READF():
                    b = stack.pop() #addr
                    a = stack.pop() #length
                    set_stack_counter(-2)
                    addr = get_var_value(b)
                    length = get_var_value(a)
                    offset = (addr+length)
                    if length > 0: 
                        s = buffer_file[addr:offset].decode('utf-8')                    
                        print_output_simulation(s, end='', istoprint=istoprint)
                elif len(stack) < 2:
                        print("WRITE impossible not enough element in stack")
                        runtime_error_counter += 1
                        error = True
                else:
                    b = stack.pop() #addr
                    a = stack.pop() #length
                    addr = get_var_value(b)
                    length = get_var_value(a)
                    set_stack_counter(-2)
                    offset = (addr+length) 
                    s = mem[addr:offset].decode('utf-8')
                    #print(s, end='')
                    print_output_simulation(s, end='', istoprint=istoprint)
                ip += 1
            elif op['type']==get_OP_SYSCALL0():
                syscall_number = stack.pop()
                set_stack_counter(-1)
                if syscall_number == 39:
                    stack.append(os.getpid())
                    set_stack_counter()
                else:
                    print(f"unknown syscall0 number: {syscall_number}")
                    runtime_error_counter += 1
                    error = True      
                stack.append(exit_code)
                set_stack_counter()          
                ip += 1
            elif op['type']==get_OP_SYSCALL1():
                syscall_number = stack.pop()
                exit_code = stack.pop()
                set_stack_counter(-2)
                if syscall_number == 60:
                    break
                else:
                    print(f"unknown syscall1: {syscall_number}")
                    runtime_error_counter += 1
                    error = True
                stack.append(exit_code)
                set_stack_counter()                   
                ip += 1 
            elif op['type']==get_OP_SYSCALL2():
                print("not implemented yet!")
                runtime_error_counter += 1
                error = True    
                stack.append(exit_code) 
                set_stack_counter()             
                ip += 1                     
            elif op['type']==get_OP_SYSCALL3():
                syscall_number = stack.pop()
                arg1 = stack.pop()
                arg2 = stack.pop()
                arg3 = stack.pop()
                set_stack_counter(-3)
                if syscall_number == 1:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    s = mem[buffer:buffer+count].decode('utf-8')
                    if fd == 1:
                        #print(s, end='')
                        print_output_simulation(s, end='', istoprint=istoprint)
                    elif fd == 2:
                        #print(s, end='', file=sys.stderr)
                        print_output_simulation(s, end='', file=sys.stderr, istoprint=istoprint)
                    else:
                        print(f"unknown file descriptor: {fd}")
                        runtime_error_counter += 1
                        error = True
                    stack.append(exit_code) 
                    set_stack_counter()
                elif syscall_number == 0:
                    fd = arg1
                    buffer = arg2
                    count = arg3
                    if fd == 0:
                        s = sys.stdin.readline()
                        mem[buffer:buffer+len(s)] = s.encode('utf-8')
                        buffer += len(s)
                        stack.append(len(s))
                        set_stack_counter()
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
                set_stack_counter()             
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL5():
                print("not implemented yet!")
                error = True                
                stack.append(exit_code)
                set_stack_counter()             
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL6():
                print("not implemented yet!")
                error = True                
                stack.append(exit_code) 
                set_stack_counter()             
                ip += 1  
            elif op['type']==get_OP_CHAR():
                stack.append(op['value'])
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_STRING():
                bstr = bytes(op['value'], 'utf-8')
                strlen = len(bstr)
                stack.append(strlen)
                set_stack_counter()
                if 'addr' not in op:
                    str_ptr = str_buf_ptr+str_size
                    op['addr'] = str_ptr
                    mem[str_ptr:str_ptr+strlen] = bstr
                    str_size += strlen
                    assert str_size <= get_STR_CAPACITY(), "String buffer overflow!"
                stack.append(op['addr'])
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_VAR():
                ip += 1
            elif op['type']==get_OP_IDVAR():
                stack.append(op['value'])
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_ARGC():
                stack.append(argc)
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_ARGV():
                stack.append(argv_buf_ptr)
                set_stack_counter()
                ip += 1

            elif op['type']==get_OP_ASSIGN_VAR():
                if len(stack) < 1:
                    print("! impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    a = stack.pop()
                    set_stack_counter(-1)
                    a_value = get_var_value(a)
                    var = op['value'][1:]
                    var_struct[var]['value'] = a_value
                    stack.append(var_struct[var]['value']) 
                    set_stack_counter()
                ip += 1                                         
            elif op['type']==get_OP_VARTYPE():              
                ip += 1
            elif op['type']==get_OP_ROTATE():
                if len(stack) < 3:
                    print("! impossible not enough element in stack")
                    runtime_error_counter += 1
                    error = True
                else:
                    c = stack.pop()
                    b = stack.pop()
                    a = stack.pop()
                    set_stack_counter(-3)
                    stack.append(b)
                    stack.append(c)
                    stack.append(a)
                    set_stack_counter(3)
                ip += 1
            elif op['type']==get_OP_OPEN():
                b = stack.pop() #addr
                a = stack.pop() #length
                addr = get_var_value(b)
                length = get_var_value(a)
                set_stack_counter(-2)
                offset = (addr+length) 
                s = mem[addr:offset].decode('utf-8')
                fd = os.open(s, os.O_RDONLY)
                #print(files_struct, op)
                stack.append(fd)
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_OPENW():
                b = stack.pop() #addr
                a = stack.pop() #length
                addr = get_var_value(b)
                length = get_var_value(a)
                set_stack_counter(-2)
                offset = (addr+length) 
                s = mem[addr:offset].decode('utf-8')
                fd = os.open(s, os.O_CREAT|os.O_WRONLY|os.O_TRUNC)
                stack.append(fd)
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_READF():
                a = stack.pop()
                set_stack_counter(-1)
                fd = get_var_value(a)
                buffer_file = bytearray(NULL_POINTER_PADDING + BUFFER_SIZE)
                readbuf = os.read(fd, BUFFER_SIZE)
                buflen = len(readbuf)
                if buflen == 0:
                    stack.append(0)
                    stack.append(0)
                else:
                    stack.append(buflen)
                    op['addr'] = buf_file_ptr
                    buffer_file[buf_file_ptr:buflen] = readbuf
                    stack.append(op['addr'])
                    #print(buffer_file)
                op['index'] = files_struct[fd]['index']
                set_stack_counter(2)
                ip += 1
            elif op['type']==get_OP_WRITEF():
                #print(stack)
                a = stack.pop()
                fd = get_var_value(a)
                op['index'] = files_struct[fd]['index']
                b = stack.pop() #buffer length
                length = get_var_value(b)
                #c = stack.pop()
                #length = get_var_value(c)
                #offset = (addr + length)
                set_stack_counter(-2)
                writebuf = os.write(fd, buffer_file[1:length])
                stack.append(writebuf)
                set_stack_counter()
                ip += 1
            elif op['type']==get_OP_CLOSE():
                a = stack.pop()
                fd = get_var_value(a)
                set_stack_counter(-1)
                os.close(fd)
                op['index'] = files_struct[fd]['index']
                ip += 1
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")  
        # if isMem:
        #     print()
        #     print(f"memory dump {mem[:20]}")  
    #probably here need to destroy variables and argc, argv
    # initialized variables 2 values in the stack variable name and value
    # non initialized variables 1 value in the stack but can be initialized later dictionary with value != None
    #need to destroy variables by reversing order of declaration
    # print("----------------------------------")  
    #print(stack)
    # print("----------------------------------")  
    return stack, error, exit_code  

# program = [{'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}, {'type': 41, 'value': 'Test\n', 'loc': ('./tests/macro1.porth', 7, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 7, 10), 'value': 'WRITE', 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 11, 1), 'value': 13, 'jmp': None}, {'type': 0, 'loc': ('./tests/macro1.porth', 15, 1), 'value': 12, 'jmp': None}, {'type': 12, 'loc': ('./tests/macro1.porth', 19, 7), 'value': '<', 'jmp': None}, {'type': 5, 'loc': ('./tests/macro1.porth', 19, 9), 'value': 'IF', 'jmp': None}, {'type': 41, 'value': 'test2 number 1  < number 2\n', 'loc': ('./tests/macro1.porth', 20, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 20, 32), 'value': 'WRITE', 'jmp': None}, {'type': 7, 'loc': ('./tests/macro1.porth', 21, 1), 'value': 'ELSE', 'jmp': None}, {'type': 41, 'value': 'test2 number 1 >= number 2\n', 'loc': ('./tests/macro1.porth', 22, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 22, 32), 'value': 'WRITE', 'jmp': None}, {'type': 6, 'loc': ('./tests/macro1.porth', 23, 1), 'value': 'END', 'jmp': None}, {'type': 41, 'value': 'Hello World!\n', 'loc': ('./tests/macro1.porth', 4, 2)}, {'type': 32, 'loc': ('./tests/macro1.porth', 4, 18), 'value': 'WRITE', 'jmp': None}]
# print(len(program))
# simulate(program)