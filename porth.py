#!/usr/bin/python3
# -*- coding: utf-8 -*-

''' 
python implementation of forth language
tuned for python 3.8 
Following the description of the forth language by Charles H. Moore
http://www.forth.org/
Youtube videos from Tsoding Daily 
'''

import argparse
from porth_lexer import get_counter_error, load_program, simulate, generate_bytecode, compile
__version__ = "1.0.0"


def porthVersion():
    return f"porth version : {__version__}"



def main(args, filename):   
    error = False
    tokens=[]
    bytecode=[]
    program, tokens, isOK = load_program(filename)
    if program==None or program[0]==(None, None, None, None) or not isOK:
        error = True
    if not error and args.simulate:
        print(f"simulating...")
        stack, error = simulate(program)
        if not error:
            #print(f"stack : {stack}")
            print("simulation succeeded!")
        else:
            print("simulation failed!")
    if not error and (args.bytecode or args.compile):
        bytecode, error = generate_bytecode(program)
        if not error:
            print(f"bytecode : {bytecode}")            
            print("bytecode generated!")
        else:
            print("bytecode generation failed!")
            error = True
    if not error and args.compile:
        print(f"compiling...")
        error = compile(bytecode, args.outfile)
        if not error:
            print("compilation done!")
        else:
            print("compilation failed!")    

    if error:
        print(f"Errors found in program: {get_counter_error()}")
    if args.dump:
        print(f"dumping...")
        print(f"tokens : {tokens}")
        print(f"stack : {stack}")
        print(f"bytecode : {bytecode}")    
        print(f"errors : {get_counter_error()}")      
        print("dumping done!")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="porth is a python3 forth language simulation")
    parser.add_argument('-V', '--version', help='Display the version of porth', action='version', version=porthVersion())
    parser.add_argument('-c', '--compile', help='compile', action="store_true", required=False)
    parser.add_argument('-d', '--dump', help='dump', action="store_true", required=False)
    parser.add_argument('-b', '--bytecode', help='generate bytecode', action="store_true", required=False)    
    parser.add_argument('-s', '--simulate', help='simulate', action="store_true", required=False)
    parser.add_argument('-i', '--inputfile', help='intput file', required=True)
    parser.add_argument('-o', '--outfile', help='output file', default="output", required=False)
    args = parser.parse_args()
    #program=[push(51), push(32), add(), dump(), push(528), push(140), sub(), dump()]
    program = args.inputfile
    main(args, program)
