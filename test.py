#!/usr/bin/pypy3

import sys
import os
import subprocess
import shlex

def cmd_run_echoed(cmd, **kwargs):
    print("[CMD] %s" % " ".join(map(shlex.quote, cmd)))
    try : 
        run=  subprocess.run(cmd, **kwargs,)
    except subprocess.CalledProcessError as e:
        run= e

    return run

def gentxt():
    for entry in os.scandir("tests/"):
        porth_ext = '.porth'
        if entry.is_file() and entry.path.endswith(porth_ext):
            print(f'[INFO] generating txt file for {entry.path}')
            txt_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/gentxt/") + ".txt"
            exe_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/gentxt/")
            f= open(txt_path, "wb")
            cmd_run_echoed(["./porth.py", "-r", "-i", entry.path, "-o",  exe_path], check=True)
            com_output = cmd_run_echoed([exe_path], capture_output=True, check=True).stdout
            f.write(com_output)
            f.close()
    for entry in os.scandir("bin/gentxt"):
        txt_ext = ".txt"
        if entry.is_file() and not entry.path.endswith(txt_ext):
            os.system(f"rm {entry.path}")

def get_args(args_path, sim=False):
    args = ""
    if os.path.exists(args_path):    
        if sim:

            args_list = open(args_path, "r").read().split()
            for arg in args_list:
                args += " -p " + arg + " "            
        else:
            args = open(args_path, "r").read()
    return args

def get_input(input_path):
    input_data = None
    if os.path.exists(input_path):    
        input_data = open(input_path, "rb").read()
    return input_data

def test():
    sim_failed = 0
    com_failed = 0
    com_libc_failed = 0
    for entry in os.scandir("tests/"):
        porth_ext = '.porth'
        if entry.is_file() and entry.path.endswith(porth_ext):
            print(f'[INFO] Testing {entry.path}')

            txt_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/") + ".txt"
            exe_path = entry.path[:-len(porth_ext)].replace("tests/", "./bin/")
            args_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/") + ".args"
            input_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/") + ".input"
            expected_output = None
            with open(txt_path, "rb") as f:
                expected_output = f.read()
            args = get_args(args_path, sim=True)
            sim_args = ["./porth.py", "-s", "-i", entry.path, "-o", exe_path]
            sim_args.extend(shlex.split(args))
            input_data = get_input(input_path) 
            sim_output = cmd_run_echoed(sim_args, input=input_data, capture_output=True, check=True).stdout
            if sim_output != expected_output:
                sim_failed += 1
                print("[ERROR] Unexpected simulation output")
                print("  Expected:")
                print(f"   {expected_output}")
                print("  Actual:")
                print(f"    {sim_output}")
            args = get_args(args_path, sim=False)
            com_args = ["./porth.py", "-c", "-i", entry.path, "-o",  exe_path]
            cmd_run_echoed(com_args, check=True)
            com_args = [exe_path]
            com_args.extend(shlex.split(args))     
            com_output = cmd_run_echoed(com_args, input=input_data, capture_output=True, check=True).stdout
            print('______________')            
            if com_output != expected_output:
                com_failed += 1
                print("[ERROR] Unexpected compilation output 1 ")
                print("  Expected:")
                print(f"    {expected_output}")
                print("  Actual:")
                print(f"    {com_output}")

            #compilation with libc
            com_libc_args = ["./porth.py", "-c", "-l", "-i", entry.path, "-o",  exe_path]
            cmd_run_echoed(com_libc_args, check=True)
            com_libc_args = [exe_path]
            com_libc_args.extend(shlex.split(args))     
            com_output = cmd_run_echoed(com_libc_args, input=input_data, capture_output=True, check=True).stdout
            print('______________')            
            if com_output != expected_output:
                com_libc_failed += 1
                print("[ERROR] Unexpected compilation with libc output 1 ")
                print("  Expected:")
                print(f"    {expected_output}")
                print("  Actual:")
                print(f"    {com_output}")

    print()
    print(f"Simulation failed: {sim_failed}, Compilation failed: {com_failed}, Compilation with libc failed: {com_libc_failed}")


def record():
    for entry in os.scandir("tests/"):
        porth_ext = '.porth'
        exe_path = entry.path[:-len(porth_ext)].replace("tests/", "bin/")
        if entry.is_file() and entry.path.endswith(porth_ext):
            sim_output = cmd_run_echoed(["./porth.py", "-s", "-i", entry.path, "-o", exe_path], capture_output=True, check=True).stdout
            txt_path = entry.path[:-len(porth_ext)] + ".txt"
            print(f"[INFO] Saving output to {txt_path}")
            with open(txt_path, "wb") as txt_file:
                txt_file.write(sim_output)

def usage(exe_name):
    print("Usage: ./test.py [SUBCOMMAND]")
    print("SUBCOMMANDS:")
    print("    test          Run the tests. (Default when no subcommand is provided)")
    print("    record        Record expected output of the tests.")
    print("    gentxt        Generate text files from simulation as reference.")
    print("    help          Print this message to stdout and exit with 0 code.")

if __name__ == '__main__':
    exe_name, *argv = sys.argv

    if len(argv) == 0:
        test()
    else:
        subcmd, *argv = argv
        if subcmd == 'record':
            record()
        elif subcmd == 'test':
            test()
        elif subcmd == 'gentxt':
            gentxt()            
        elif subcmd == 'help':
            usage(exe_name)
         
        else:
            usage(exe_name)
            print(f"[ERROR] unknown subcommand `{subcmd}`", file=sys.stderr)
            exit(1)