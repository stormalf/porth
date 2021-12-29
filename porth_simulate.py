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

def simulate_op_push(value: Any) -> None:
    global stack
    stack.append(value)
    set_stack_counter()

def simulate_op_add(op: Dict) -> None:
    global stack
    errfunction="simulate_op_add"
    if len(stack) < 2:
        #print("ADD impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)                    
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)
        stack.append(a_value + b_value)
        set_stack_counter()

def simulate_op_sub(op: Dict) -> None:
    global stack
    errfunction="simulate_op_sub"
    if len(stack) < 2:
        #print("SUB impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)                    
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(a_value - b_value)
        set_stack_counter()

def simulate_op_equal(op: Dict) -> None:
    global stack
    errfunction="simulate_op_equal"
    if len(stack) < 2:
        #print("EQUAL impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)  
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                
        stack.append(int(a_value == b_value)) 
        set_stack_counter()        

def simulate_op_dump(op: Dict, ip: int , program: List, istoprint: bool) -> None:
    global stack
    errfunction="simulate_op_dump"
    if len(stack) == 0:
        #print("stack is empty impossible to dump")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        if program[ip - 1]['type'] == get_OP_IDVAR():
            #print(var_struct[a]['value'])
            print_output_simulation(var_struct[a]['value'], istoprint=istoprint)
        else:
            #print(a)
            print_output_simulation(a, istoprint=istoprint)

def simulate_op_if(op: Dict) -> None:
    global stack
    errfunction="simulate_op_if"
    ip = None
    if len(stack) == 0:
        #print("stack is empty impossible to execute if statement")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        a_value = get_var_value(a)
        set_stack_counter(-1)
        if a_value == 0:
            if len(op) >= 2:
                ip = op['jmp']
            else:
                #print("if statement without jmp")
                generate_runtime_error(op=op, errfunction=errfunction, msgid= 1)
    return ip


def simulate_op_dup(op: Dict) -> None:
    global stack
    errfunction="simulate_op_dup"
    if len(stack) == 0:
        #print("stack is empty impossible to duplicate")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        stack.append(a_value)
        stack.append(a_value)
        set_stack_counter(2)

def simulate_op_dup2(op: Dict) -> None:
    global stack
    errfunction="simulate_op_dup2"
    if len(stack) < 2:
        #print("2DUP impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
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

def simulate_op_gt(op: Dict) -> None:
    global stack
    errfunction="simulate_op_gt"
    if len(stack) < 2:
        #print("> impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:                
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value > b_value)) 
        set_stack_counter()


def simulate_op_lt(op: Dict) -> None:
    global stack
    errfunction="simulate_op_lt"
    if len(stack) < 2:
        #print("< impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value < b_value)) 
        set_stack_counter()


def simulate_op_ge(op: Dict) -> None:
    global stack
    errfunction="simulate_op_ge"
    if len(stack) < 2:
        #print(">= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value >= b_value)) 
        set_stack_counter()

def simulate_op_le(op: Dict) -> None:
    global stack
    errfunction="simulate_op_le"
    if len(stack) < 2:
        #print("<= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value <= b_value)) 
        set_stack_counter()

def simulate_op_ne(op: Dict) -> None:
    global stack
    errfunction="simulate_op_ne"
    if len(stack) < 2:
        #print("!= impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        #if variable retrieve the content value 
        a_value = get_var_value(a)
        b_value = get_var_value(b)                  
        stack.append(int(a_value != b_value)) 
        set_stack_counter()


def simulate_op_div(op: Dict, istoprint: bool) -> None:
    global stack
    errfunction="simulate_op_div"
    if len(stack) < 2:
        #print("/ impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid= 3)
        else:
            stack.append(int(a_value / b_value))
            set_stack_counter()                 

def simulate_op_divmod(op: Dict, istoprint: bool) -> None:
    global stack
    errfunction="simulate_op_divmod"
    if len(stack) < 2:
        #print("divmod impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid= 3)
        else:
            stack.append(int(a_value / b_value))
            stack.append(int(a_value % b_value))
            set_stack_counter(2)

def simulate_op_mul(op: Dict) -> None:
    global stack
    errfunction="simulate_op_mul"
    if len(stack) < 2:
        #print("* impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(int(a_value * b_value))
        set_stack_counter()

def simulate_op_load(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_load"
    if len(stack) < 1:
        #print("load impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        addr = stack.pop()
        a_value = get_var_value(addr)
        set_stack_counter(-1)
        byte = mem[a_value]
        stack.append(byte)
        set_stack_counter()

def simulate_op_store(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_store"
    if len(stack) < 2:
        #print("store impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        value = stack.pop() 
        addr = stack.pop() 
        set_stack_counter(-2)                
        a_value = get_var_value(value)                
        b_value = get_var_value(addr)                                
        mem[b_value] = a_value & 0xFF

def simulate_op_load16(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_load16"
    if len(stack) < 1:
        #print("load16 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        addr = get_var_value(a)                
        _bytes = bytearray(2)
        for offset in range(0,2):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()


def simulate_op_store16(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_store16"
    if len(stack) < 2:
        #print("store16 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        store_value = get_var_value(a)                
        store_value16 = store_value.to_bytes(length=2, byteorder="little",  signed=(store_value < 0))
        store_addr16 = get_var_value(b)                
        for byte in store_value16:
            mem[store_addr16] = byte
            store_addr16 += 1


def simulate_op_load32(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_load32"
    if len(stack) < 1:
        #print("load32 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        addr = get_var_value(a)                
        _bytes = bytearray(4)
        for offset in range(0,4):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()


def simulate_op_store32(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_store32"
    if len(stack) < 2:
        #print("store32 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        store_value = get_var_value(a)                
        store_value32 = store_value.to_bytes(length=4, byteorder="little",  signed=(store_value < 0))
        store_addr32 = get_var_value(b)                
        for byte in store_value32:
            mem[store_addr32] = byte
            store_addr32 += 1


def simulate_op_load64(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_load64"
    if len(stack) < 1:
        #print("load64 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        set_stack_counter(-1)
        addr = get_var_value(a)                
        _bytes = bytearray(8)
        for offset in range(0,8):
            _bytes[offset] = mem[addr + offset]
        stack.append(int.from_bytes(_bytes, byteorder="little"))
        set_stack_counter()

def simulate_op_store64(op: Dict) -> None:
    global stack, mem
    errfunction="simulate_op_store64"
    if len(stack) < 2:
        #print("store64 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        a = stack.pop()
        b = stack.pop()
        set_stack_counter(-2)
        store_value = get_var_value(a)                
        store_value64 = store_value.to_bytes(length=8, byteorder="little",  signed=(store_value < 0))
        store_addr64 = get_var_value(b)                
        for byte in store_value64:
            mem[store_addr64] = byte
            store_addr64 += 1

def simulate_op_swap(op: Dict) -> None:
    global stack
    errfunction="simulate_op_swap"
    if len(stack) < 2:
        #print("swap impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(b_value)
        stack.append(a_value)
        set_stack_counter(2)

def simulate_op_shl(op: Dict) -> None:
    global stack
    errfunction="simulate_op_shl"
    if len(stack) < 2:
        #print("shl impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value << b_value)
        set_stack_counter()

def simulate_op_shr(op: Dict) -> None:
    global stack
    errfunction="simulate_op_shr"
    if len(stack) < 2:
        #print("shr impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value >> b_value)
        set_stack_counter()

def simulate_op_orb(op: Dict) -> None:
    global stack
    errfunction="simulate_op_orb"
    if len(stack) < 2:
        #print("orb impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value | b_value)
        set_stack_counter()

def simulate_op_andb(op: Dict) -> None:
    global stack
    errfunction="simulate_op_andb"
    if len(stack) < 2:
        #print("andb impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        stack.append(a_value & b_value)
        set_stack_counter()

def simulate_op_over(op: Dict) -> None:
    global stack
    errfunction="simulate_op_over"
    if len(stack) < 2:
        #print("over impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                
        stack.append(a_value)
        stack.append(b_value)
        stack.append(a_value)
        set_stack_counter(3)

def simulate_op_mod(op: Dict, istoprint: bool) -> None:
    global stack
    errfunction="simulate_op_mod"
    if len(stack) < 2:
        #print("mod impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid= 0)
    else:
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-2)
        a_value = get_var_value(a)
        b_value = get_var_value(b)                    
        if b_value == 0:
            #print(RUNTIME_ERROR[RUN_DIV_ZERO])
            print_output_simulation(RUNTIME_ERROR[RUN_DIV_ZERO], istoprint=istoprint)
            generate_runtime_error(op=op, errfunction=errfunction, msgid=3)
        else:
            stack.append(a_value % b_value)
            set_stack_counter()

def simulate_op_write(op: Dict, ip: int, program: List, istoprint: bool) -> None:
    global stack, mem, buffer_file
    errfunction="simulate_op_write"
    if program[ip-1]['type']==get_OP_CHAR():
        if len(stack) < 1:
            #print("WRITE impossible not enough element in stack")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
        else:
            #print(chr(program[ip - 1]['value']), end="")
            a = stack.pop()
            set_stack_counter(-1)
            a_value = get_var_value(a)
            #print_output_simulation(chr(program[ip - 1]['value']), end="", istoprint=istoprint)
            print_output_simulation(chr(a_value), end="", istoprint=istoprint)
    elif program[ip-1]['type']==get_OP_READF():
        if len(stack) < 2:
            #print("READF impossible not enough element in stack")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
        else:
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
        #print("WRITE impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
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


def simulate_op_readf(op: Dict, ip: int, program: List, istoprint: bool) -> None:
    global stack, mem, buffer_file, buf_file_ptr
    errfunction="simulate_op_readf"
    if len(stack) < 1:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
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

def simulate_op_writef(op: Dict, ip: int, program: List, istoprint: bool) -> None:
    global stack, mem, buffer_file, buf_file_ptr
    errfunction="simulate_op_writef"
    if len(stack) < 2:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        #print(stack)
        a = stack.pop()
        b = stack.pop() #buffer length                
        set_stack_counter(-2)                
        fd = get_var_value(a)
        op['index'] = files_struct[fd]['index']
        length = get_var_value(b)
        writebuf = os.write(fd, buffer_file[1:length])
        stack.append(writebuf)
        set_stack_counter()
 
def simulate_op_close(op: Dict) -> None:
    global stack, files_struct
    errfunction="simulate_op_close"
    if len(stack) < 1:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        a = stack.pop()
        fd = get_var_value(a)
        set_stack_counter(-1)
        os.close(fd)
        op['index'] = files_struct[fd]['index']


def simulate_op_rotate(op: Dict) -> None:
    global stack
    errfunction="simulate_op_rotate"
    if len(stack) < 3:
        #print("! impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        c = stack.pop()
        b = stack.pop()
        a = stack.pop()
        set_stack_counter(-3)
        stack.append(b)
        stack.append(c)
        stack.append(a)
        set_stack_counter(3)

def simulate_op_open(op: Dict) -> None:
    global stack, files_struct, mem
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
        offset = (addr+length) 
        s = mem[addr:offset].decode('utf-8')
        fd = os.open(s, os.O_RDONLY)
        #print(files_struct, op)
        stack.append(fd)
        set_stack_counter()

def simulate_op_openw(op: Dict) -> None:
    global stack, mem
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
        offset = (addr+length) 
        s = mem[addr:offset].decode('utf-8')
        fd = os.open(s, os.O_CREAT|os.O_WRONLY|os.O_TRUNC)
        stack.append(fd)
        set_stack_counter()
        
def simulate_op_syscall0(op: Dict) -> None:
    global stack, files_struct
    errfunction="simulate_op_syscall0"
    if len(stack) < 1:
        #print("SYSCALL0 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
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

def simulate_op_syscall1(op: Dict) -> bool:
    global stack, files_struct
    exit = False
    errfunction="simulate_op_syscall1"
    if len(stack) < 2:
        #print("SYSCALL1 impossible not enough element in stack")
        generate_runtime_error(op=op, errfunction=errfunction, msgid=0)
    else:
        syscall_number = stack.pop()
        exit_code = stack.pop()
        set_stack_counter(-2)
        if syscall_number == 60:
            exit = True
        else:
            print(f"unknown syscall1: {syscall_number}")
            generate_runtime_error(op=op, errfunction=errfunction, msgid=4)
            stack.append(exit_code)
            set_stack_counter()                   
    return exit




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


