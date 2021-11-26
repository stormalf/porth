# porth

python3 forth language following youtube tutorial from Tsoding Daily.
Many thanks to him for his tutorial and youtube videos very interesting and helpful.

Link to the gitlab repo : https://gitlab.com/tsoding/porth/-/blob/master/porth.py

Youtube link for the first Tutorial : https://youtu.be/8QP2fDBIxjM?list=PLpM-Dvs8t0VbMZA7wW9aR3EtBqe2kinu4

Note that I'm using Github Copilot that helps a lot to reduce the need of copy/paste by suggesting often the correct way to write code.
It uses often the same syntax that I used in the current code. Sometimes it still suggests a code already implemented but probably it will be improved later to correct this behaviour. Very cool!

## porth compiler usage

python3 porth.py --help

    usage: porth.py [-h] [-V] [-c] [-d] [-s] [-r] [-l] -i INPUTFILE [-o OUTFILE]

    porth is a python3 forth language simulation

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of porth
    -c, --compile         compile
    -d, --dump            dump
    -s, --simulate        simulate
    -r, --run             compile and run
    -l, --libc            using gcc and libc
    -i INPUTFILE, --inputfile INPUTFILE
                            intput file
    -o OUTFILE, --outfile OUTFILE
                            output file

Example to compile :

    python3 porth.py -c -i pgm1.porth -o pgm1

Example after refactoring into folders :

    python3 porth.py -c -i tests/pgm11.porth -o bin/pgm11

## Lexing

It shows all errors in a file and don't compile or simulate if error found during lexing phasis:

python3 porth.py -c -i pgm3.porth -o pgm3

    Error Code 1 Token . is forbidden in first position in file pgm3.porth, line 1 column 1
    Error Code 1 Token - is forbidden in first position in file pgm3.porth, line 2 column 1
    Error Code 1 Token + is forbidden in first position in file pgm3.porth, line 3 column 1
    Error Code 1 Token - is forbidden in first position in file pgm3.porth, line 4 column 1
    Error Code 1 Token . is forbidden in first position in file pgm3.porth, line 5 column 1

python3 porth.py -c -i pgm4.porth -o pgm4

    Error Code 0 Unknown word: "test" at line 1, column 1 in file pgm4.porth
    Error Code 0 Unknown word: fqkqjqs at line 2, column 1 in file pgm4.porth
    Error Code 0 Unknown word: akfkjkj at line 3, column 1 in file pgm4.porth
    Error Code 0 Unknown word: "''( at line 4, column 1 in file pgm4.porth
    Error Code 0 Unknown word: ) at line 6, column 1 in file pgm4.porth

Example with simulation instead of compilation :

    python3 porth.py -s -i pgm7.porth -o pgm7

    simulating...
    777
    simulation succeeded!

## language features

Keyword, operators, and constants are defined in the language.

    NUMBER : is pushed to the stack
    + : operator pops 2 values from the stack and push the sum of them
    - : operator pops 2 values from the stack and push the difference of them
    . : operator pops 1 value from the stack and print it
    = : operator pops 2 values from the stack and push 1 if equality and 0 otherwise
    > : operator pops 2 values from the stack and push 1 if the first one is greater than the second one and 0 otherwise
    < : operator pops 2 values from the stack and push 1 if the first one is less than of second one and 0 otherwise
    IF: keyword to create a conditional statement
    ELSE: keyword to create a conditional statement if the condition is false
    END: keyword to close a conditional statement
    DUP: keyword to duplicate the top of the stack
    WHILE: keyword to create a loop followed by a conditional statement
    DO: keyword to open the loop if the condition is true
    LOOP: keyword to close the loop
    COMMENTS : are ignored by the compiler 3 possible comments allowed for now : //, # and ;
    MEM: keyword to push the address of the beginning of the memory onto the stack
    @: operator loads value from the memory
    $: operator stores value to the memory
    2DUP: keyword to duplicate the top 2 values of the stack
    SWAP: keyword to swap the top 2 values of the stack
    DROP: keyword to drop the top value of the stack
    RETURN: keyword to end the program (calls syscall1)
    SHR: shift right bits
    SHL: shift left bits
    ORB: bitwise or
    ANDB: bitwise and
    DIV: integer division
    MUL: integer multiplication
    MOD: integer modulo
    !=: operator pops 2 values from the stack and push 1 if not equality and 0 otherwise
    >=: operator pops 2 values from the stack and push 1 if the first one is greater or equal than the second one and 0 otherwise
    <=: operator pops 2 values from the stack and push 1 if the first one is less or equal than the second one and 0 otherwise
    ": starts and end a string, not that for now it doesn't allow a // or a # in the string due to the fact that they are comments

## release notes

1.0.0 initial version

1.0.1 restructuring the code, adding simple IF/END statement and removing generate_bytecode function (no adding value and duplicated code)

1.0.2 adding ELSE statement

1.0.3 adding a kind of AST Tree

1.0.4 adding DUP, > and < operators

1.0.5 fixing GT/LT and adding WHILE/DO/END (Episode 3)

1.0.6 adding comment types // # ; (Episode 4) and refactoring files into separate folders

1.0.7 adding compilation with gcc and libc (printf) or without gcc (using ld and sycall) new parameter -l for that

1.0.8 fixing a bug about xref_program assigned before reference and adding -r parameter to run automatically after a successful compilation

1.0.9 Be careful big restructuration passing from tuples to dictionary! Not sure to keep the AST tree sample (not sure that it can be useful). (Episode 4 just the beginning!)

1.0.10 adding a new feature to the language : the memory. Issue with /usr/bin/ld: bin/mem1.o: relocation R_X86_64_32S against `.bss' can not be used when making a PIE object; recompile with -fPIE solved by adding -static to the gcc flags and ld flags

1.0.11 Not following the same operators for loading and storing memory : adding $ operator for loading and @ operator for storing and adding syscall3 (syscall with 3 parameters) and syscall1 (syscall with 1 parameter) for exit.

1.0.12 Implementing 2DUP and RETURN keyword to exit the program with specific return value. Fixing issue with WHILE and "error: symbol `addr_39' undefined" and adding other syscall but only for compiling (not simulation mode)

1.0.13 Removing -a option and adding new keyword DROP, SWAP, refactoring code to separate simulate and compile functions into different files

1.0.14 Adding OVER keyword and rule110 example (end episode 5)

1.0.15 Adding >=, <=, !=, MOD, MUL and DIV operators

1.0.16 Refactoring code, using dictionary and creating a global file porth_globals.py to store global variables and functions

1.0.17 Adding strings for now only " are allowed and recognized as strings. Removing ";" as comment I didn't use it really.
Adding also global runtime counter error. Adding test.py file to test the language. Still one issue with -l the exe generated with libc has strange behaviour it seems to work but no stdout or stderr!!!! To solve later if I found why ?

1.0.18 finally found how to solve the empty output when compiling with libc! full information in this link :
https://coderedirect.com/questions/239430/printf-without-newline-in-assembly explain that you have to flush! After adding the flush it works now for both gcc and without gcc! (2 days lose of time for this issue!)

1.0.19 adding annotations to the code using typing. And taken in account into test the compilation with libc and without libc.
And adding the possibility to generate the .txt automatically (to use carefully and probably in a new folder)

## TODO

Trying to implement similar language but using ANTLR4.
