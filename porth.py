#!/usr/bin/pypy3
# -*- coding: utf-8 -*-

''' 
python implementation of forth language
tuned for python 3.8 
Following the description of the forth language by Charles H. Moore
http://www.forth.org/
Youtube videos from Tsoding Daily 
'''

import argparse
import os
import sys
from porth_lexer import load_program
from porth_compiler import compile
from porth_interpreter import simulate, get_runtime_error
from porth_error import check_errors, check_warnings, print_errors, print_warnings, get_counter_error, get_counter_warning
from typing import *

__version__ = "1.0.30"


def porthVersion() -> str:
    return f"porth version : {__version__}"


def run_program(filename: str, parameter: List) -> None:
    os.system(filename + ' ' + ' '.join(par[0] for par in parameter))

def main(args, filename: str) -> None:   
    error = False
    tokens=[]
    stack = []
    exit_code = 0
    #args.parameter.insert(0, [args.outfile])
    program, tokens, isOK = load_program(filename)
    if isOK==False:
        error = True
    # if args.ast and not error:
    #     print_ast(tokens)        
    if not error and args.simulate:
        #print("simulating...")

        stack, error, exit_code = simulate(program, args.parameter, args.outfile)
        if error:
            print("simulation failed!")
            print(f"Errors found during runtime simulation: {get_runtime_error()}")
    if not error and (args.compile or args.run):
        #print("compiling...")
        error = compile(program, args.outfile, args.libc, args.parameter)
        if not error:
            #print("compilation done!")
            if args.run:
                run_program(args.outfile, args.parameter)
        else:
            print("compilation failed!")   
    if check_errors():
        print_errors()
        print(f"Errors found in program : {get_counter_error()}")
    if args.warning:
        if check_warnings(filename):
            print_warnings()
            print(f"Warnings found in program {filename} : {get_counter_warning()}")            
    if args.dump:
        print("----------------------------------")
        print(f"dumping...")
        print(f"tokens : {tokens}")
        print(f"stack : {stack}")
        print(f"errors : {get_counter_error()}")  
        print(f"warnings : {get_counter_warning()}")      
        print("----------------------------------")        
    sys.exit(exit_code)   

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="porth is a python3 forth language simulation")
    parser.add_argument('-V', '--version', help='Display the version of porth', action='version', version=porthVersion())
    parser.add_argument('-c', '--compile', help='compile', action="store_true", required=False)
    parser.add_argument('-d', '--dump', help='dump', action="store_true", required=False)
    parser.add_argument('-s', '--simulate', help='simulate', action="store_true", required=False)
    parser.add_argument('-r', '--run', help='compile and run', action="store_true", required=False)      
    #parser.add_argument('-a', '--ast', help='ast tree', action="store_true", required=False)  
    parser.add_argument('-l', '--libc', help='using gcc and libc', action="store_true", required=False)      
    parser.add_argument('-i', '--inputfile', help='intput file', required=True)
    parser.add_argument('-o', '--outfile', help='output file', default="output", required=False)
    parser.add_argument('-w', '--warning', help='display warnings', action="store_true", required=False)  
    parser.add_argument('-p', '--parameter', help='parameter for execution', default=[], required=False, action='append',  nargs='+')        
    args = parser.parse_args()
    program = args.inputfile
    main(args, program)