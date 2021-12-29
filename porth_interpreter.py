#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import FileIO
import sys
import os
from typing import Tuple
from porth_globals import *
from typing import *
from porth_error import check_runtime_errors, generate_runtime_error, get_runtime_error, print_runtime_errors
from porth_simulate import *

#simulate the program execution without compiling it. To be able to re-use the simulate function to detect some warnings and errors
#the output is printed only if the function is requested with istoprint=True (default behaviour)
def simulate(program: List, parameter: List, outfile:str, istoprint=True) -> Tuple[List,bool, int]:
    global exit_code, MAX_LOOP_SECURITY, var_struct, BUFFER_SIZE, stack, mem, mem_buf_ptr
    #print(program)
    errfunction="simulate"
    conditions_stack = {}
    assert get_OPS() == get_MAX_OPS(),  "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())  
    #stack=[]
    error = False
    #isMem = False
    ip = 0
    str_size= NULL_POINTER_PADDING
    #mem = bytearray(NULL_POINTER_PADDING +  get_STR_CAPACITY() +  get_ARGV_CAPACITY() + get_MEM_CAPACITY())
    #buffer_file = bytearray(NULL_POINTER_PADDING + BUFFER_SIZE)
    outlist=[outfile]
    parameter.insert(0, outlist)
    argv_buf_ptr = NULL_POINTER_PADDING + get_STR_CAPACITY()
    str_buf_ptr  = NULL_POINTER_PADDING
    #buf_file_ptr = NULL_POINTER_PADDING
    #mem_buf_ptr  = NULL_POINTER_PADDING + get_STR_CAPACITY() + get_ARGV_CAPACITY()
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
    if not error:
        while ip < len(program):
            op = program[ip]
            #print(stack)
            if check_runtime_errors():
                print_runtime_errors()
                print(f"Errors found during runtime simulation: {get_runtime_error()}")                
                sys.exit(-1)
            if op['type']==get_OP_PUSH():
                ip += 1
                simulate_op_push(op['value'])
            elif op['type']==get_OP_ADD():
                simulate_op_add(op)        
                ip += 1
            elif op['type']==get_OP_SUB():
                simulate_op_sub(op)
                ip += 1                
            elif op['type']==get_OP_EQUAL():
                simulate_op_equal(op)
                ip += 1                
            elif op['type']==get_OP_DUMP():
                simulate_op_dump(op, ip, program, istoprint)
                ip += 1   
            elif op['type']==get_OP_IF():
                ip += 1                
                newip = simulate_op_if(op)
                if newip != None:
                    ip = newip
            elif op['type']==get_OP_ELSE():
                if len(op) >= 2:
                    ip = op['jmp']
                else:
                    #print("else statement without jmp")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid= 1)
            elif op['type']==get_OP_END():
                if len(op) >= 2:
                    ip = op['jmp']
                else:
                    #print("end statement without jmp")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid= 1)
            elif op['type']==get_OP_DUP():
                simulate_op_dup(op)
                ip += 1 
            elif op['type']==get_OP_DUP2():
                simulate_op_dup2(op)
                ip += 1                 
            elif op['type']==get_OP_GT():
                simulate_op_gt(op)
                ip += 1        
            elif op['type']==get_OP_LT():
                simulate_op_lt(op)
                ip += 1   
            elif op['type']==get_OP_GE(): 
                simulate_op_ge(op)               
                ip += 1
            elif op['type']==get_OP_LE():
                simulate_op_le(op)
                ip += 1
            elif op['type']==get_OP_NE():
                simulate_op_ne(op)
                ip += 1
            elif op['type']==get_OP_DIV():
                simulate_op_div(op, istoprint)
                ip += 1
            elif op['type']==get_OP_DIVMOD():
                simulate_op_divmod(op, istoprint)
                ip += 1                
            elif op['type']==get_OP_MUL():
                simulate_op_mul(op)
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
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=2)
                if a_value == 0:
                    if len(op) >= 2:
                        ip = op['jmp']
                    else:
                        #print("do statement without jmp")
                        generate_runtime_error(op=op, errfunction=errfunction, msgid=1)
                else:
                    ip += 1    
            elif op['type']==get_OP_MEM():#when using mem the address is put on the stack and never removed 
                #isMem = True
                stack.append(mem_buf_ptr)
                set_stack_counter()
                ip += 1  
            elif op['type']==get_OP_LOAD():
                simulate_op_load(op)
                ip += 1                    
            elif op['type']==get_OP_STORE():
                simulate_op_store(op)
                #print("store!")
                # value = stack.pop() 
                # addr = stack.pop() 
                # set_stack_counter(-2)                
                # a_value = get_var_value(value)                
                # b_value = get_var_value(addr)                                
                # mem[b_value] = a_value & 0xFF
                #print(stack, a_value, b_value, mem[b_value:1])
                ip += 1  
            elif op['type']==get_OP_LOAD16():
                simulate_op_load16(op)
                ip += 1                    
            elif op['type']==get_OP_STORE16():
                simulate_op_store16(op)
                ip += 1                   
            elif op['type']==get_OP_LOAD32():
                simulate_op_load32(op)
                ip += 1                     
            elif op['type']==get_OP_STORE32():
                simulate_op_store32(op)
                ip += 1                
            elif op['type']==get_OP_LOAD64():
                simulate_op_load64(op)
                ip += 1
            elif op['type']==get_OP_STORE64():
                simulate_op_store64(op)
                ip += 1
            elif op['type']==get_OP_SWAP():
                simulate_op_swap(op)
                ip += 1        
            elif op['type']==get_OP_SHL():
                simulate_op_shl(op)
                ip += 1      
            elif op['type']==get_OP_SHR():
                simulate_op_shr(op)
                ip += 1
            elif op['type']==get_OP_ORB():
                simulate_op_orb(op)
                ip += 1
            elif op['type']==get_OP_ANDB():
                simulate_op_andb(op)
                ip += 1         
            elif op['type']==get_OP_DROP():
                if len(stack) < 1:
                    #print("DROP impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                else:
                    stack.pop()
                    set_stack_counter(-1)
                ip += 1
            elif op['type']==get_OP_OVER():
                simulate_op_over(op)
                ip += 1
            elif op['type']==get_OP_MOD():
                simulate_op_mod(op, istoprint)
                ip += 1
            elif op['type']==get_OP_EXIT():
                if len(stack) < 1:
                    #print("EXIT impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                syscall_number = 60
                a = stack.pop()
                set_stack_counter(-1)
                exit_code = get_var_value(a)
                break
            elif op['type']==get_OP_WRITE():
                simulate_op_write(op=op, ip=ip, program=program, istoprint=istoprint)
                # if program[ip-1]['type']==get_OP_CHAR():
                #     if len(stack) < 1:
                #         #print("WRITE impossible not enough element in stack")
                #         generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                #     #print(chr(program[ip - 1]['value']), end="")
                #     a = stack.pop()
                #     set_stack_counter(-1)
                #     a_value = get_var_value(a)
                #     #print_output_simulation(chr(program[ip - 1]['value']), end="", istoprint=istoprint)
                #     print_output_simulation(chr(a_value), end="", istoprint=istoprint)
                # elif program[ip-1]['type']==get_OP_READF():
                #     if len(stack) < 2:
                #         #print("READF impossible not enough element in stack")
                #         generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                #     b = stack.pop() #addr
                #     a = stack.pop() #length
                #     set_stack_counter(-2)
                #     addr = get_var_value(b)
                #     length = get_var_value(a)
                #     offset = (addr+length)
                #     if length > 0: 
                #         s = buffer_file[addr:offset].decode('utf-8')                    
                #         print_output_simulation(s, end='', istoprint=istoprint)
                # elif len(stack) < 2:
                #         #print("WRITE impossible not enough element in stack")
                #         generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                # else:
                #     b = stack.pop() #addr
                #     a = stack.pop() #length
                #     addr = get_var_value(b)
                #     length = get_var_value(a)
                #     set_stack_counter(-2)
                #     offset = (addr+length) 
                #     s = mem[addr:offset].decode('utf-8')
                #     #print(s, end='')
                #     print_output_simulation(s, end='', istoprint=istoprint)
                ip += 1
            elif op['type']==get_OP_SYSCALL0():
                if len(stack) < 1:
                    #print("SYSCALL0 impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                syscall_number = stack.pop()
                set_stack_counter(-1)
                if syscall_number == 39:
                    stack.append(os.getpid())
                    set_stack_counter()
                else:
                    #print(f"unknown syscall0 number: {syscall_number}")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
                stack.append(exit_code)
                set_stack_counter()          
                ip += 1
            elif op['type']==get_OP_SYSCALL1():
                if len(stack) < 2:
                    #print("SYSCALL1 impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                syscall_number = stack.pop()
                exit_code = stack.pop()
                set_stack_counter(-2)
                if syscall_number == 60:
                    break
                else:
                    print(f"unknown syscall1: {syscall_number}")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
                stack.append(exit_code)
                set_stack_counter()                   
                ip += 1 
            elif op['type']==get_OP_SYSCALL2():
                #print("not implemented yet!")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=5)
                ip += 1                     
            elif op['type']==get_OP_SYSCALL3():
                if len(stack) < 4:
                    #print("SYSCALL3 impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                #save_stack = stack.copy()
                else:
                    syscall_number = stack.pop()
                    arg1 = stack.pop()
                    arg2 = stack.pop()
                    arg3 = stack.pop()
                    set_stack_counter(-4)
                    #print(op, stack,syscall_number, arg1, arg2, arg3, mem[arg2:100])
                    if arg2 == 0:
                        #print(f"arg2 cannot be 0 {op}, {program[ip - 1]}, {program[ip - 2]}, {program[ip - 3]}, {save_stack}")
                        generate_runtime_error(op=op, errfunction=errfunction, msgid=6)
                    elif syscall_number == 1:
                        fd = get_var_value(arg1)
                        buffer = get_var_value(arg2)
                        count = get_var_value(arg3)
                        #print(mem[buffer:10], fd, buffer, count)
                        s = mem[buffer:buffer+count].decode('utf-8')
                        if fd == 1:
                            #print(s, end='')
                            print_output_simulation(s, end='', istoprint=istoprint)
                        elif fd == 2:
                            #print(s, end='', file=sys.stderr)
                            print_output_simulation(s, end='', file=sys.stderr, istoprint=istoprint)
                        else:
                            os.write(fd, mem[buffer:buffer+count])
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
                            generate_runtime_error(op=op, errfunction=errfunction, msgid=7)
                    else:
                        #print(f"unknown syscall3: {syscall_number}")
                        generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
                ip += 1    
            elif op['type']==get_OP_SYSCALL4():
                #print("not implemented yet!")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=5)             
                stack.append(exit_code) 
                set_stack_counter()             
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL5():
                #print("not implemented yet!")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=5)
                stack.append(exit_code)
                set_stack_counter()             
                ip += 1                                                     
            elif op['type']==get_OP_SYSCALL6():
                #print("not implemented yet!")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=5)
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
                if program[ip - 1]['type'] != get_OP_VAR():
                    #print(op)
                    stack.append(op['value'])
                    set_stack_counter()
                    #print(stack, op, get_OP_VAR())
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
                    #print("! impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                else:
                    a = stack.pop()
                    set_stack_counter(-1)
                    a_value = get_var_value(a)
                    var = op['value'][1:]
                    typevar = var_struct[var]['type']
                    if check_valid_value(type=typevar, value=a_value):
                        var_struct[var]['value'] = a_value
                    else:
                        print(f"! invalid value {a_value} for the variable type: {typevar}")
                        generate_runtime_error(op=op, errfunction=errfunction, msgid=8)
                ip += 1                                         
            elif op['type']==get_OP_VARTYPE():              
                ip += 1
            elif op['type']==get_OP_ROTATE():
                simulate_op_rotate(op=op)
                ip += 1
            elif op['type']==get_OP_OPEN():
                simulate_op_open(op=op)
                ip += 1
            elif op['type']==get_OP_OPENW():
                if len(stack) < 2:
                    #print("! impossible not enough element in stack")
                    generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
                else:
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
                simulate_op_readf(op=op, ip=ip, program=program, istoprint=istoprint)
                ip += 1
            elif op['type']==get_OP_WRITEF():
                simulate_op_writef(op=op, ip=ip, program=program, istoprint=istoprint)
                ip += 1
            elif op['type']==get_OP_CLOSE():
                simulate_op_close(op)
                ip += 1
            else:
                ip += 1                
                error = True
                print(f"Unknown opcode: {op}")          # if isMem:
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