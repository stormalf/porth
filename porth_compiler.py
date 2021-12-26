#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from porth_globals import *
from porth_assembler import *

#DIV_BY_0="Division by zero!"


#compile the bytecode using nasm and gcc (for printf usage)
def compile(bytecode: List, outfile: str, libc: bool = True, parameter: List = []) -> bool:
    global exit_code, var_struct
    bss_var = []
    strs = []
    assert get_OPS() == get_MAX_OPS(), "Max Opcode implemented! expected " + str(get_MAX_OPS()) + " but got " + str(get_OPS())   
    asmfile = outfile + ".asm"
    output = open(asmfile, "w") 
    #
    output.write(COMMON_HEADER)
    if libc:
        output.write(HEADER) 
        #generate_read_argv(output)        
        output.write("mov [args_ptr], rsi\n")  
    else:
        output.write(HEADER2)
        output.write("mov [args_ptr], rsp\n")        
    error = False    
    for ip in range(len(bytecode)):
        op = bytecode[ip]
        output.write(f"addr_{ip}: \n")
        if op['type']==get_OP_PUSH():
            generate_push_op(output, op['value'])
        elif op['type']==get_OP_ADD():
            generate_add_op(output)
        elif op['type']==get_OP_SUB():
            generate_sub_op(output)
        elif op['type']==get_OP_EQUAL():
            generate_equal_op(output)
        elif op['type']==get_OP_IF():
            generate_if_op(output, op)
        elif op['type']==get_OP_ELSE(): 
            generate_else_op(output, op)
        elif op['type']==get_OP_END():
            generate_end_op(output, op, ip)
        elif op['type']==get_OP_DUMP():
            generate_dump_op(output, ip, libc)
        elif op['type']==get_OP_DUP():
            generate_dup_op(output)
        elif op['type']==get_OP_DUP2():
            generate_dup2_op(output)                         
        elif op['type']==get_OP_GT():
            generate_gt_op(output)              
        elif op['type']==get_OP_LT():
            generate_lt_op(output)
        elif op['type']==get_OP_GE():
            generate_ge_op(output)
        elif op['type']==get_OP_LE():
            generate_le_op(output)
        elif op['type']==get_OP_NE():
            generate_ne_op(output)
        elif op['type']==get_OP_DIV():
            generate_div_op(output, ip, libc)
        elif op['type']==get_OP_DIVMOD():
            generate_divmod_op(output, ip, libc)
        elif op['type']==get_OP_MUL(): 
            generate_mul_op(output)
        elif op['type']==get_OP_WHILE():
            output.write("; while \n")
        elif op['type']==get_OP_DO():
            generate_do_op(output, op)
        elif op['type']==get_OP_MEM(): 
            generate_mem_op(output)
        elif op['type']==get_OP_LOAD(): 
            generate_load_op(output)
        elif op['type']==get_OP_STORE(): 
            generate_store_op(output)
        elif op['type']==get_OP_LOAD16():
            generate_load16_op(output)
        elif op['type']==get_OP_STORE16():
            generate_store16_op(output)            
        elif op['type']==get_OP_LOAD32():
            generate_load32_op(output)
        elif op['type']==get_OP_STORE32():
            generate_store32_op(output)
        elif op['type']==get_OP_LOAD64():
            generate_load64_op(output)
        elif op['type']==get_OP_STORE64():
            generate_store64_op(output)
        elif op['type']==get_OP_SWAP(): 
            generate_swap_op(output)
        elif op['type']==get_OP_DROP():
            generate_drop_op(output)
        elif op['type']==get_OP_SHL():
            generate_shl_op(output)
        elif op['type']==get_OP_SHR():
            generate_shr_op(output)
        elif op['type']==get_OP_ORB():
            generate_orb_op(output)
        elif op['type']==get_OP_ANDB():
            generate_andb_op(output)
        elif op['type']==get_OP_OVER():
            generate_over_op(output)
        elif op['type']==get_OP_MOD():
            generate_mod_op(output, ip, libc)
        elif op['type']==get_OP_EXIT(): 
            generate_exit_op(output)
        elif op['type']==get_OP_WRITE():
            generate_write_op(output, bytecode[ip - 1], libc)
        elif op['type']==get_OP_SYSCALL0():
            generate_syscall0_op(output)
        elif op['type']==get_OP_SYSCALL1():    
            generate_syscall1_op(output)
        elif op['type']==get_OP_SYSCALL2():
            generate_syscall2_op(output)
        elif op['type']==get_OP_SYSCALL3():    
            generate_syscall3_op(output)
        elif op['type']==get_OP_SYSCALL4():
            generate_syscall4_op(output)
        elif op['type']==get_OP_SYSCALL5():
            generate_syscall5_op(output)
        elif op['type']==get_OP_SYSCALL6():
            generate_syscall6_op(output)
        elif op['type']==get_OP_CHAR():
            output.write("; char\n")  
            output.write(f"push {op['value']}\n")
        elif op['type']==get_OP_STRING():
            generate_string_op(output, len(op['value']), len(strs))
            strs.append(op['value'])
        elif op['type']==get_OP_VAR():
            pass
        elif op['type']==get_OP_IDVAR():
            generate_idvar_op(output, bytecode[ip - 1], op)
        elif op['type']==get_OP_ASSIGN_VAR():
            generate_assign_op(output, bytecode[ip - 1], op)  
        elif op['type'] == get_OP_ARGC():
            if libc:
                generate_argc_libc_op(output)
            else:            
                generate_argc_op(output)
        elif op['type'] == get_OP_ARGV():
            if libc:
                generate_argv_libc_op(output)
            else:
                generate_argv_op(output)
        elif op['type']==get_OP_VARTYPE():
            pass
        elif op['type']==get_OP_ROTATE():
            generate_rotate_op(output)
        elif op['type']==get_OP_OPEN():
            generate_open_op(output, op)
        elif op['type']==get_OP_CLOSE():
            generate_close_op(output, op)
        elif op['type']==get_OP_OPENW():
            generate_open_op(output, op)
        elif op['type']==get_OP_READF():
            generate_readf_op(output, op)
        elif op['type']==get_OP_WRITEF():
            generate_writef_op(output, op)
        else:
            print(f"Unknown bytecode op: {op}")    
            error = True 
    #managing infinite loop exit (one label only)
    output.write(f"jmp addr_{len(bytecode)}\n")  
    generate_infinite_loop_op(output, libc)    
    output.write(f"addr_{len(bytecode)}:\n")               
    output.write(FOOTER)
    output.write(DATA)
    for index, s in enumerate(strs):
        output.write(f"str_{index}: db {','.join(map(hex, list(bytes(s, 'utf-8'))))}, 0\n")
    #print(files_struct)
    for index in files_struct:
        output.write(f"file_{index}: db `{files_struct[index]['filename']}\\0`\n")
    for i in RUNTIME_ERROR:
        output.write(f'error_message_{i} db "{RUNTIME_ERROR[i]}", 10, 0\n')
    for i, var in enumerate(var_struct):
        if var_struct[var]['type']==OPU8 and var_struct[var]['value']!= None:
            output.write(f"{var}: db {var_struct[var]['value']}, 0\n")
        elif var_struct[var]['type']==OPU16 and var_struct[var]['value']!= None:
            output.write(f"{var}: dw {var_struct[var]['value']}, 0\n")
        elif var_struct[var]['type']==OPU32 and var_struct[var]['value']!= None:
            output.write(f"{var}: dd {var_struct[var]['value']}, 0\n")
        elif var_struct[var]['type']==OPU64 and var_struct[var]['value']!= None:
            output.write(f"{var}: dq {var_struct[var]['value']}, 0\n")   
        else:
            bss_var.append(var)  
    output.write(BSS)
    for var in bss_var:
        if var_struct[var]['type']==OPU8:
            output.write(f"{var}: resb 1\n")
        elif var_struct[var]['type']==OPU16:
            output.write(f"{var}: resw 2\n")
        elif var_struct[var]['type']==OPU32:
            output.write(f"{var}: resd 4\n")
        elif var_struct[var]['type']==OPU64:
            output.write(f"{var}: resq 8\n")
    output.write("args_ptr: resq 1\n")
    output.close()
    if libc:
        os.system(f"nasm -felf64 {asmfile}  &&  gcc -static {outfile}.o -o {outfile} ")
    else:
        os.system(f"nasm -felf64 {asmfile}  &&  ld -static {outfile}.o -o {outfile} ")
    return error