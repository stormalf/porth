from io import FileIO
import sys
import os
from typing import Tuple
from porth_globals import *
from typing import *
from porth_error import generate_runtime_error


stdoutput = ""
stack =  []
mem = bytearray(NULL_POINTER_PADDING +  get_STR_CAPACITY() +  get_ARGV_CAPACITY() + get_MEM_CAPACITY())
mem_buf_ptr  = NULL_POINTER_PADDING + get_STR_CAPACITY() + get_ARGV_CAPACITY()
buffer_file = bytearray(NULL_POINTER_PADDING + BUFFER_SIZE)
buf_file_ptr = NULL_POINTER_PADDING
argv_buf_ptr = NULL_POINTER_PADDING + get_STR_CAPACITY()
str_buf_ptr  = NULL_POINTER_PADDING
str_size = 1 #null terminated character string

control_stack = []
type_stack = []
typeint = "INT"
typefloat = "FLOAT"
typechar = "CHAR"
typebool = "BOOL"
typeptr = "PTR"
typestr = "STR"
typeunknown = "UNK"
typeidvar = "IDVAR"


def simulate_op_push(value: Any) -> List:
    global stack, type_stack
    stack.append(value)
    type_stack.append(typeint)
    set_stack_counter()
    return stack.copy()

def simulate_op_add(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_add"
    if len(stack) < 2:
        #print("ADD impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)                    
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #print(stack, type_stack)
        tb = type_stack.pop()
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for ADD operation {ta}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        elif tb not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for ADD operation {tb}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)
        stack.append(a_value + b_value)
        type_stack.append(typeint)
        set_stack_counter()
    return stack.copy()

def simulate_op_sub(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_sub"
    if len(stack) < 2:
        #print("SUB impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)                    
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SUB operation {ta}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        elif tb not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SUB operation {tb}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(a_value - b_value)
        set_stack_counter()        
        if ta == typeptr or tb == typeptr:
            type_stack.append(typeptr)
        else:
            type_stack.append(typeint)
    return stack.copy()

def simulate_op_equal(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_equal"
    if len(stack) < 2:
        #print("EQUAL impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)  
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for EQUAL operation {ta}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        elif tb not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for EQUAL operation {tb}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                
        stack.append(int(a_value == b_value)) 
        type_stack.append(typebool)
        set_stack_counter()
    return stack.copy()        

def simulate_op_dump(op: Dict, ip: int , program: List, istoprint: bool) -> List:
    global stack, type_stack
    errfunction="simulate_op_dump"
    if len(stack) == 0:
        #print("stack is empty impossible to dump")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in(typeint, typeptr, typechar, typeidvar, typebool):
            print(f"TypeChecking: incorrect type on stack for DUMP operation {ta}. Expecting {typeint} or {typeptr} or {typechar} or {typeidvar} or {typebool}")
            sys.exit(1)
        if program[ip - 1]['type'] == get_OP_IDVAR():
            #print(var_struct[a]['value'])
            print_output_simulation(var_struct[a]['value'], istoprint=istoprint)
        else:
            #print(a)
            print_output_simulation(a, istoprint=istoprint)
    return stack.copy()

def simulate_op_if(op: Dict) -> Tuple[List, Union[None, int]]:
    global stack, type_stack
    errfunction="simulate_op_if"
    ip = None
    if len(stack) == 0:
        #print("stack is empty impossible to execute if statement")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        a_value = get_var_value(a)
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in(typebool, typeint):
            print(f"TypeChecking: incorrect type on stack for IF operation {ta}. Expecting {typebool} or {typeint}")
            sys.exit(1)
        if a_value == 0:
            if len(op) >= 2:
                ip = op['jmp']
            else:
                #print("if statement without jmp")
                generate_runtime_error(op=op, errfunction=errfunction, msgid= 1)
    return stack.copy(), ip


def simulate_op_dup(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_dup"
    if len(stack) == 0:
        #print("stack is empty impossible to duplicate")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DUP operation {ta}. Expecting {typeint} or {typechar} or {typeptr} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        stack.append(a_value)
        stack.append(a_value)
        set_stack_counter(2)
        type_stack.append(ta)
        type_stack.append(ta)            
    return stack.copy()

def simulate_op_dup2(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_dup2"
    if len(stack) < 2:
        #print("2DUP impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in (typeint, typechar, typeptr, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DUP2 operation {tb}. Expecting {typeint} or {typechar} or {typeptr} or {typebool} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DUP2 operation {ta}. Expecting {typeint} or {typechar} or {typeptr} or {typebool} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)               
        stack.append(a_value)
        type_stack.append(ta)
        stack.append(b_value)
        type_stack.append(tb)
        stack.append(a_value)
        type_stack.append(ta)
        stack.append(b_value)
        type_stack.append(tb)
        set_stack_counter(4)
    return stack.copy()

def simulate_op_gt(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_gt"
    if len(stack) < 2:
        #print("> impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:                
        b = stack.pop()
        a = stack.pop()
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for GT operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for GT operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value > b_value))
        type_stack.append(typebool) 
        set_stack_counter()
    return stack.copy()


def simulate_op_lt(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_lt"
    if len(stack) < 2:
        #print("< impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for LT operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for LT operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value < b_value)) 
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()


def simulate_op_ge(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_ge"
    if len(stack) < 2:
        #print(">= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for GE operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for GE operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value >= b_value)) 
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()

def simulate_op_le(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_le"
    if len(stack) < 2:
        #print("<= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for LE operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for LE operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value <= b_value)) 
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()

def simulate_op_ne(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_ne"
    if len(stack) < 2:
        #print("!= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar, typeptr):
            print(f"TypeChecking: incorrect type on stack for NE operation {tb}. Expecting {typeint} or {typeidvar} or {typeptr}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar, typeptr):
            print(f"TypeChecking: incorrect type on stack for NE operation {ta}. Expecting {typeint} or {typeidvar} or {typeptr}")
            sys.exit(1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value != b_value)) 
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()


def simulate_op_div(op: Dict, istoprint: bool) -> List:
    global stack, type_stack
    errfunction="simulate_op_div"
    if len(stack) < 2:
        #print("/ impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DIV operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DIV operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid= 3)
        else:
            stack.append(int(a_value / b_value))
            set_stack_counter()
            type_stack.append(typeint)                 
    return stack.copy()

def simulate_op_divmod(op: Dict, istoprint: bool) -> List:
    global stack, type_stack
    errfunction="simulate_op_divmod"
    if len(stack) < 2:
        #print("divmod impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DIVMOD operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for DIVMOD operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid= 3)
        else:
            stack.append(int(a_value / b_value))
            type_stack.append(typeint)
            stack.append(int(a_value % b_value))
            type_stack.append(typeint)
            set_stack_counter(2)
    return stack.copy()

def simulate_op_mul(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_mul"
    if len(stack) < 2:
        #print("* impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for MUL operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for MUL operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(int(a_value * b_value))
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_load(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_load"
    if len(stack) < 1:
        #print("load impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        addr = stack.pop()
        a_value = get_var_value(addr)
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in(typeptr, typeint):
            print(f"TypeChecking: incorrect type on stack for LOAD operation {ta}. Expecting {typeptr} or {typeint}")
            sys.exit(1)
        byte = mem[a_value]
        stack.append(byte)
        type_stack.append(typeint)
        set_stack_counter()
    return stack.copy()

def simulate_op_store(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_store"
    if len(stack) < 2:
        #print("store impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        value = stack.pop() 
        addr = stack.pop() 
        set_stack_counter(-2)    
        tb = type_stack.pop()
        if tb not in(typeint, typeptr, typeidvar, typechar, typebool):
            print(f"TypeChecking: incorrect type on stack for STORE operation {tb}. Expecting {typeint} or {typeptr} or {typeidvar} or {typechar} or {typebool}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeptr, typeint):
            print(f"TypeChecking: incorrect type on stack for STORE operation {ta}. Expecting {typeptr} or {typeint}")
            sys.exit(1)            
        a_value = get_var_value(value)                
        b_value = get_var_value(addr)                                
        mem[b_value] = a_value & 0xFF
    return stack.copy()    

def simulate_op_load16(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_load16"
    if len(stack) < 1:
        #print("load16 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta != typeptr:
            print(f"TypeChecking: incorrect type on stack for LOAD16 operation {ta}. Expecting {typeptr}")
            sys.exit(1)
        addr = get_var_value(a)                
        _bytes = bytearray(2)
        for offset in range(0,2):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_store16(op: Dict) -> List:
    global stack, mem
    errfunction="simulate_op_store16"
    if len(stack) < 2:
        #print("store16 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for STORE16 operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta != typeptr:
            print(f"TypeChecking: incorrect type on stack for STORE16 operation {ta}. Expecting {typeptr}")
            sys.exit(1)
        store_value = get_var_value(a)                
        store_value16 = store_value.to_bytes(length=2, byteorder="little",  signed=(store_value < 0))
        store_addr16 = get_var_value(b)                
        for byte in store_value16:
            mem[store_addr16] = byte
            store_addr16 += 1
    return stack.copy()

def simulate_op_load32(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_load32"
    if len(stack) < 1:
        #print("load32 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta != typeptr:
            print(f"TypeChecking: incorrect type on stack for LOAD32 operation {ta}. Expecting {typeptr}")
            sys.exit(1)
        addr = get_var_value(a)                
        _bytes = bytearray(4)
        for offset in range(0,4):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_store32(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_store32"
    if len(stack) < 2:
        #print("store32 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for STORE32 operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta != typeptr:
            print(f"TypeChecking: incorrect type on stack for STORE32 operation {ta}. Expecting {typeptr}")
            sys.exit(1)
        store_value = get_var_value(a)                
        store_value32 = store_value.to_bytes(length=4, byteorder="little",  signed=(store_value < 0))
        store_addr32 = get_var_value(b)                
        for byte in store_value32:
            mem[store_addr32] = byte
            store_addr32 += 1
    return stack.copy()

def simulate_op_load64(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_load64"
    if len(stack) < 1:
        #print("load64 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in(typeptr, typeint):
            print(f"TypeChecking: incorrect type on stack for LOAD64 operation {ta}. Expecting {typeptr} or {typeint}")
            sys.exit(1)
        addr = get_var_value(a)                
        _bytes = bytearray(8)
        for offset in range(0,8):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        #print(op, addr, int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_store64(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_store64"
    if len(stack) < 2:
        #print("store64 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for STORE64 operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeptr, typeint):
            print(f"TypeChecking: incorrect type on stack for STORE64 operation {ta}. Expecting {typeptr} or {typeint}")
            sys.exit(1)
        store_value = get_var_value(a)                
        store_value64 = store_value.to_bytes(length=8, byteorder="little",  signed=(store_value < 0))
        store_addr64 = get_var_value(b)                
        for byte in store_value64:
            mem[store_addr64] = byte
            store_addr64 += 1
    return stack.copy()

def simulate_op_swap(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_swap"
    if len(stack) < 2:
        #print("swap impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in (typeint, typeptr, typechar, typebool):
            print(f"TypeChecking: incorrect type on stack for SWAP operation {tb}. Expecting {typeint} or {typeptr} or {typechar} or {typebool}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in (typeint, typeptr, typechar, typebool):
            print(f"TypeChecking: incorrect type on stack for SWAP operation {ta}. Expecting {typeint} or {typeptr} or {typechar} or {typebool}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(b_value)
        type_stack.append(tb)
        stack.append(a_value)
        type_stack.append(ta)
        set_stack_counter(2)
    return stack.copy()

def simulate_op_shl(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_shl"
    if len(stack) < 2:
        #print("shl impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SHL operation {tb}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SHL operation {ta}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value << b_value)
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_shr(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_shr"
    if len(stack) < 2:
        #print("shr impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SHR operation {tb}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SHR operation {ta}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value >> b_value)
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_orb(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_orb"
    if len(stack) < 2:
        #print("orb impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typebool, typeidvar):  
            print(f"TypeChecking: incorrect type on stack for ORB operation {tb}. Expecting {typebool} or {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typebool, typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for ORB operation {ta}. Expecting {typebool} or {typeint} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value | b_value)
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()

def simulate_op_andb(op: Dict) -> List:
    global stack
    errfunction="simulate_op_andb"
    if len(stack) < 2:
        #print("andb impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for ANDB operation {tb}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typebool, typeidvar):
            print(f"TypeChecking: incorrect type on stack for ANDB operation {ta}. Expecting {typeint} or {typebool} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value & b_value)
        set_stack_counter()
        type_stack.append(typebool)
    return stack.copy()

def simulate_op_over(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_over"
    if len(stack) < 2:
        #print("over impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in (typeint, typeptr, typechar, typebool):
            print(f"TypeChecking: incorrect type on stack for OVER operation {tb}. Expecting {typeint} or {typeptr} or {typechar} or {typebool}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in (typeint, typeptr, typechar, typebool):
            print(f"TypeChecking: incorrect type on stack for OVER operation {ta}. Expecting {typeint} or {typeptr} or {typechar} or {typebool}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                
        stack.append(a_value)
        type_stack.append(ta)
        stack.append(b_value)
        type_stack.append(tb)
        stack.append(a_value)
        type_stack.append(ta)
        set_stack_counter(3)
    return stack.copy()

def simulate_op_mod(op: Dict, istoprint: bool) -> List:
    global stack, type_stack
    errfunction="simulate_op_mod"
    if len(stack) < 2:
        #print("mod impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for MOD operation {tb}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for MOD operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid=3)
        else:
            stack.append(a_value % b_value)
            set_stack_counter()
            type_stack.append(typeint)
    return stack.copy()

def simulate_op_write(op: Dict, ip: int, program: List, istoprint: bool) -> List:
    global stack, mem, buffer_file, type_stack
    errfunction="simulate_op_write"
    if program[ip-1]['type']==get_OP_CHAR():
        if len(stack) < 1:
            #print("WRITE impossible not enough element in stack")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
        else:
            #print(chr(program[ip - 1]['value']), end="")
            a = stack.pop()
            set_stack_counter(-1)
            ta = type_stack.pop()
            if ta != typechar:
                print(f"TypeChecking: incorrect type on stack for WRITE operation {ta}. Expecting {typechar}")
                sys.exit(1)
            a_value = get_var_value(a)
            #print_output_simulation(chr(program[ip - 1]['value']), end="", istoprint=istoprint)
            print_output_simulation(chr(a_value), end="", istoprint=istoprint)
    elif program[ip-1]['type']==get_OP_READF():
        addr = program[ip - 1]['addr']
        if len(stack) < 1:
            #print("READF impossible not enough element in stack")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
        else:
            #b = stack.pop() #addr
            a = stack.pop() #length
            set_stack_counter(-2)
            #tb = type_stack.pop()
            #if tb != typeptr:
            #    print(f"TypeChecking: incorrect type on stack for READF operation {tb}. Expecting {typeptr}")
            #    sys.exit(1)
            ta = type_stack.pop()
            if ta not in(typeint, typeidvar):
                print(f"TypeChecking: incorrect type on stack for READF operation {ta}. Expecting {typeint} or {typeidvar}")
                sys.exit(1)
            #addr = get_var_value(b)
            length = get_var_value(a)
            offset = (addr+length)
            if length > 0: 
                s = buffer_file[addr:offset].decode('utf-8')                    
                print_output_simulation(s, end='', istoprint=istoprint)
    elif len(stack) < 2:
        #print("WRITE impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        b = stack.pop() #addr
        a = stack.pop() #length
        set_stack_counter(-2)        
        if b == "BUFFER_FILE":
            addr = buf_file_ptr
            length = get_var_value(a)
            tb = type_stack.pop()
            if tb != typeptr:
                print(f"TypeChecking: incorrect type on stack for WRITE operation {tb}. Expecting {typeptr}")
                sys.exit(1)
            ta = type_stack.pop()
            if ta != typeint:
                print(f"TypeChecking: incorrect type on stack for WRITE operation {ta}. Expecting {typeint}")
                sys.exit(1)
            offset = (addr+length) 
            s = buffer_file[addr:offset].decode('utf-8')

        else:
            addr = get_var_value(b)
            length = get_var_value(a)
            tb = type_stack.pop()
            if tb != typeptr:
                print(f"TypeChecking: incorrect type on stack for WRITE operation {tb}. Expecting {typeptr}")
                sys.exit(1)
            ta = type_stack.pop()
            if ta != typeint:
                print(f"TypeChecking: incorrect type on stack for WRITE operation {ta}. Expecting {typeint}")
                sys.exit(1)
            offset = (addr+length) 
            s = mem[addr:offset].decode('utf-8')
        #print(s, end='')
        print_output_simulation(s, end='', istoprint=istoprint)
    return stack.copy()


def simulate_op_readf(op: Dict, ip: int, program: List, istoprint: bool) -> List:
    global stack, mem, buffer_file, buf_file_ptr, type_stack
    errfunction="simulate_op_readf"
    if len(stack) < 1:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        fd = get_var_value(a)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for READF operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        buffer_file = bytearray(NULL_POINTER_PADDING + BUFFER_SIZE)
        readbuf = os.read(fd, BUFFER_SIZE)
        buflen = len(readbuf)
        if buflen == 0:
            stack.append("BUFFER_FILE")
            type_stack.append(typeptr)
            stack.append(0)
            type_stack.append(typeint)            
        else:
            op['addr'] = buf_file_ptr
            buffer_file[buf_file_ptr:buf_file_ptr+buflen] = readbuf
            #stack.append(op['addr'])
            stack.append("BUFFER_FILE")
            type_stack.append(typeptr)
            stack.append(buflen)
            type_stack.append(typeint)
            #print(buffer_file)
        op['index'] = files_struct[fd]['index']
        set_stack_counter(2)
    return stack.copy()

def simulate_op_writef(op: Dict, ip: int, program: List, istoprint: bool) -> List:
    global stack, mem, buffer_file, buf_file_ptr, type_stack
    errfunction="simulate_op_writef"
    if len(stack) < 3:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        #print(stack)
        a = stack.pop() #fd
        addr = stack.pop() # buffer address
        b = stack.pop() #buffer length     
        if addr == "BUFFER_FILE":
            addr = buf_file_ptr
        else:
            sys.exit(1)
        set_stack_counter(-3)                
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for WRITEF operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        tb = type_stack.pop()
        if tb not in(typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for WRITEF operation {tb}. Expecting {typeptr} or {typeidvar}")
            sys.exit(1)
        tc = type_stack.pop()
        if tc not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for WRITEF operation {tc}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        fd = get_var_value(a)
        op['index'] = files_struct[fd]['index']
        length = get_var_value(b)
        writebuf = os.write(fd, buffer_file[addr:length])
        stack.append(writebuf)
        type_stack.append(typeint)
        set_stack_counter()
    return stack.copy()
 
def simulate_op_close(op: Dict) -> List:
    global stack, files_struct, type_stack
    errfunction="simulate_op_close"
    if len(stack) < 1:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        a = stack.pop()
        fd = get_var_value(a)
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for CLOSE operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        os.close(fd)
        op['index'] = files_struct[fd]['index']
    return stack.copy()

def simulate_op_rotate(op: Dict) -> List:
    global stack, type_stack
    errfunction="simulate_op_rotate"
    if len(stack) < 3:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        c = stack.pop()
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-3)
        tc = type_stack.pop()
        if tc not in (typeint, typechar, typeptr):
            print(f"TypeChecking: incorrect type on stack for ROTATE operation {tc}. Expecting {typeint}, {typechar} or {typeptr}")
            sys.exit(1)
        tb = type_stack.pop()
        if tb not in (typeint, typechar, typeptr):
            print(f"TypeChecking: incorrect type on stack for ROTATE operation {tb}. Expecting {typeint}, {typechar} or {typeptr}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in (typeint, typechar, typeptr):
            print(f"TypeChecking: incorrect type on stack for ROTATE operation {ta}. Expecting {typeint}, {typechar} or {typeptr}")
            sys.exit(1)
        stack.append(b)
        type_stack.append(tb)
        stack.append(c)
        type_stack.append(tc)
        stack.append(a)
        type_stack.append(ta)
        set_stack_counter(3)
    return stack.copy()

def simulate_op_open(op: Dict) -> List:
    global stack, files_struct, mem, type_stack
    errfunction="simulate_op_open"
    if len(stack) < 2:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        b = stack.pop() #addr
        a = stack.pop() #length
        addr = get_var_value(b)
        length = get_var_value(a)
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb not in(typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for OPEN operation {tb}. Expecting {typeptr} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for OPEN operation {ta}. Expecting {typeint} or {typeidvar}")
            sys.exit(1)
        offset = (addr+length) 
        s = mem[addr:offset].decode('utf-8')
        fd = os.open(s, os.O_RDONLY)
        #print(files_struct, op)
        stack.append(fd)
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()

def simulate_op_openw(op: Dict) -> List:
    global stack, mem, type_stack
    errfunction="simulate_op_openw"
    if len(stack) < 2:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        b = stack.pop() #addr
        a = stack.pop() #length
        addr = get_var_value(b)
        length = get_var_value(a)
        set_stack_counter(-2)
        tb = type_stack.pop()
        if tb != typeptr:
            print(f"TypeChecking: incorrect type on stack for OPEN operation {tb}. Expecting {typeptr}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta != typeint:
            print(f"TypeChecking: incorrect type on stack for OPEN operation {ta}. Expecting {typeint}")
            sys.exit(1)
        offset = (addr+length) 
        s = mem[addr:offset].decode('utf-8')
        fd = os.open(s, os.O_CREAT|os.O_WRONLY|os.O_TRUNC)
        stack.append(fd)
        set_stack_counter()
        type_stack.append(typeint)
    return stack.copy()
        
def simulate_op_syscall0(op: Dict) -> List:
    global stack, files_struct, exit_code, type_stack
    errfunction="simulate_op_syscall0"
    if len(stack) < 1:
        #print("SYSCALL0 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        syscall_number = stack.pop()
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta != typeint:
            print(f"TypeChecking: incorrect type on stack for SYSCALL0 operation {ta}. Expecting {typeint}")
            sys.exit(1)
        if syscall_number == 39:
            stack.append(os.getpid())
            set_stack_counter()
            type_stack.append(typeint)
        else:
            #print(f"unknown syscall0 number: {syscall_number}")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
            stack.append(exit_code)
            set_stack_counter()       
            type_stack.append(typeint)   
    return stack.copy()

def simulate_op_syscall1(op: Dict) -> Tuple[List, bool]:
    global stack, files_struct, type_stack
    exit = False
    errfunction="simulate_op_syscall1"
    if len(stack) < 2:
        #print("SYSCALL1 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        syscall_number = stack.pop()
        ta = type_stack.pop()
        if ta != typeint:
            print(f"TypeChecking: incorrect type on stack for SYSCALL1 operation {ta}. Expecting {typeint}")
            sys.exit(1)
        exit_code = stack.pop()
        tb = type_stack.pop()
        if tb != typeint:
            print(f"TypeChecking: incorrect type on stack for SYSCALL1 operation {tb}. Expecting {typeint}")
            sys.exit(1)
        set_stack_counter(-2)
        if syscall_number == 60:
            exit = True
        else:
            print(f"unknown syscall1: {syscall_number}")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
            stack.append(exit_code)
            set_stack_counter()    
            type_stack.append(typeint)               
    return stack.copy(), exit

def simulate_op_syscall3(op: Dict, istoprint: bool) -> List:
    global stack, files_struct, mem, exit_code, type_stack
    errfunction="simulate_op_syscall3"
    if len(stack) < 4:
        #print("SYSCALL3 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
        stack.append(exit_code)
        set_stack_counter()                    
        type_stack.append(typeint)
        #save_stack = stack.copy()
    else:
        syscall_number = stack.pop()
        arg1 = stack.pop()
        arg2 = stack.pop()
        arg3 = stack.pop()
        set_stack_counter(-4)
        td = type_stack.pop()
        if td not in (typeint, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SYSCALL3 operation {td}. Expecting {typeint} or {typeptr} or {typeidvar}")
            sys.exit(1)
        tc = type_stack.pop()
        if tc not in(typeint, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SYSCALL3 operation {tc}. Expecting {typeint} or {typeptr} or {typeidvar}")
            sys.exit(1)
        tb = type_stack.pop()
        if tb not in (typeptr, typeint, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SYSCALL3 operation {tb}. Expecting {typeptr} or {typeint} or {typeidvar}")
            sys.exit(1)
        ta = type_stack.pop()
        if ta not in(typeint, typeptr, typeidvar):
            print(f"TypeChecking: incorrect type on stack for SYSCALL3 operation {ta}. Expecting {typeint} or {typeptr} or {typeidvar}")
            sys.exit(1)
        #print(op, stack,syscall_number, arg1, arg2, arg3, mem[arg2:100])
        if arg2 == 0:
            #print(f"arg2 cannot be 0 {op}, {program[ip - 1]}, {program[ip - 2]}, {program[ip - 3]}, {save_stack}")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=6)
            stack.append(exit_code)
            set_stack_counter()
            type_stack.append(typeint)
        elif syscall_number == 1:
            fd = get_var_value(arg1)
            buffer = get_var_value(arg2)
            count = get_var_value(arg3)            
            if buffer == "BUFFER_FILE":
                s = buffer_file[buf_file_ptr:buf_file_ptr+count].decode('utf-8')
            #print(mem[buffer:10], fd, buffer, count)
            else: 
                s = mem[buffer:buffer+count].decode('utf-8')
            if fd == 1:
                #print(s, end='')
                print_output_simulation(s, end='', istoprint=istoprint)
                stack.append(exit_code)
                set_stack_counter()   
                type_stack.append(typeint)                         
            elif fd == 2:
                #print(s, end='', file=sys.stderr)
                print_output_simulation(s, end='', file=sys.stderr, istoprint=istoprint)
                stack.append(exit_code)
                set_stack_counter()       
                type_stack.append(typeint)                     
            else:
                if buffer == "BUFFER_FILE":
                    os.write(fd, buffer_file[buf_file_ptr:buf_file_ptr+count])
                else:
                    os.write(fd, mem[buffer:buffer+count])
                stack.append(exit_code)
                set_stack_counter()       
                type_stack.append(typeint)                     
                # stack.append(exit_code) 
                # set_stack_counter()
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
                type_stack.append(typeint)
            else:
                print(f"unknown file descriptor: {fd}")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=7)
                stack.append(exit_code)
                set_stack_counter()
                type_stack.append(typeint)
        else:
            #print(f"unknown syscall3: {syscall_number}")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
            stack.append(exit_code)
            set_stack_counter()           
            type_stack.append(typeint)            
    return stack.copy()

def simulate_op_itos(op: Dict) -> List:
    global stack, mem, str_buf_ptr, str_size, var_struct, type_stack
    errfunction="simulate_op_itos"
    if len(stack) < 1:
        #print("itos impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        a = stack.pop() #value to convert to string
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta != typeint:
            print(f"TypeChecking: incorrect type on stack for ITOS operation {ta}. Expecting {typeint}")
            sys.exit(1)
        if a in var_struct:
            var = a
        else:
            var = None
        a_value = get_var_value(a)
        if a_value == None:
            #print(f"itos: {a} is not a valid value")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=9)
            return
        if var != None:
            typev = var_struct[var]['type']
            if check_valid_value(type=typev, value=a_value) == False:
                generate_runtime_error(op=op, errfunction=errfunction, msgid=10)
                return
        s = str(a_value) #convert to string
        bstr = bytes(s, 'utf-8')
        strlen = len(bstr)
        stack.append(strlen)
        set_stack_counter()
        type_stack.append(typeint)
        if 'addr' not in op:
            str_ptr = str_buf_ptr+str_size
            op['addr'] = str_ptr
            mem[str_ptr:str_ptr+strlen] = bstr
            str_size += strlen
            assert str_size <= get_STR_CAPACITY(), "String buffer overflow!"
            stack.append(op['addr'])
            set_stack_counter()
            type_stack.append(typeptr)
    return stack.copy()

def simulate_op_len(op: Dict, ip: int, program:List) -> List:
    global stack, mem, str_buf_ptr, str_size, var_struct, type_stack
    errfunction="simulate_op_len"
    if len(stack) < 1:
        #print("len impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        a = stack.pop() #value to retrieve length
        set_stack_counter(-1)
        ta = type_stack.pop()
        if ta not in (typeint, typeptr):
            print(f"TypeChecking: incorrect type on stack for LEN operation {ta}. Expecting {typeint} or {typeptr}")
            sys.exit(1)
        if a in var_struct:
            var = a
        else:
            var = None
        a_value = get_var_value(a)
    
        if a_value == None:
            #print(f"itos: {a} is not a valid value")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=9)
            return
        if var != None:
            typev = var_struct[var]['type']
            if check_valid_value(type=typev, value=a_value) == False:
                generate_runtime_error(op=op, errfunction=errfunction, msgid=10)
                return
        #if the previous instruction is a string, the a_value is the address into memory
        # for now we drop it and ge the previous one!
        if program[ip - 1]['type'] == get_OP_STRING():
            if len(stack) < 1:
                #print("len impossible not enough element in stack")
                generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
            else:
                a = stack.pop() #value to retrieve length
                set_stack_counter(-1)
                ta = type_stack.pop()
                if ta != typeint:
                    print(f"TypeChecking: incorrect type on stack for LEN operation {ta}. Expecting {typeint}")
                    sys.exit(1)
                stack.append(a)
                set_stack_counter()
                type_stack.append(typeint)
        else: 
            s = str(a_value) #convert to string
            strlen = len(s)
            stack.append(strlen)
            set_stack_counter()
            type_stack.append(typeint)
    return stack.copy()


#print only if requested
def print_output_simulation(value, file: FileIO = sys.stdout, end: str = None, istoprint: bool = True) -> None:
    global stdoutput
    if istoprint:
        if end is None:
            print(value, file=file)
            stdoutput = stdoutput + str(value)
        else:
            print(value, end=end, file=file)
            stdoutput = stdoutput + str(value) + end