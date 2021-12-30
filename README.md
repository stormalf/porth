# porth

python3 forth language following youtube tutorial from Tsoding Daily.
Many thanks to him for his tutorial and youtube videos very interesting and helpful.

Link to the gitlab repo : https://gitlab.com/tsoding/porth/-/blob/master/porth.py

Youtube link for the first Tutorial : https://youtu.be/8QP2fDBIxjM?list=PLpM-Dvs8t0VbMZA7wW9aR3EtBqe2kinu4

Note that I'm using Github Copilot that helps a lot to reduce the need of copy/paste by suggesting often the correct way to write code.
It uses often the same syntax that I used in the current code. Sometimes it still suggests a code already implemented but probably it will be improved later to correct this behaviour. Very cool!

## porth compiler usage

./porth.py --help

    usage: porth.py [-h] [-V] [-c] [-d] [-s] [-r] [-l] -i INPUTFILE [-o OUTFILE] [-w] [-p PARAMETER [PARAMETER ...]]

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
    -w, --warning         display warnings
    -p PARAMETER [PARAMETER ...], --parameter PARAMETER [PARAMETER ...]
                            parameter for execution

Example to compile :

    ./porth.py -c -i pgm1.porth -o pgm1

Example after refactoring into folders :

    ./porth.py -c -i tests/pgm11.porth -o bin/pgm11

Example to compile and run passing parameters for execution :

    ./porth.py -r -l -i tests/string4.porth -o bin/string4 -p titi -p toto -p test -p tata

## Lexing

It shows all errors in a file and don't compile or simulate if error found during lexing phasis:

./porth.py -c -i pgm4.porth -o pgm4

    Error Code 0 Unknown word: "test" at line 1, column 1 in file pgm4.porth
    Error Code 0 Unknown word: fqkqjqs at line 2, column 1 in file pgm4.porth
    Error Code 0 Unknown word: akfkjkj at line 3, column 1 in file pgm4.porth
    Error Code 0 Unknown word: "''( at line 4, column 1 in file pgm4.porth
    Error Code 0 Unknown word: ) at line 6, column 1 in file pgm4.porth

Example with simulation instead of compilation :

    ./porth.py -s -i pgm7.porth -o pgm7
    777

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
    COMMENTS : are ignored by the compiler 3 possible comments allowed for now : //, #.
    MEM: keyword to push the address of the beginning of the memory onto the stack
    $ or $8: operator loads value from the memory 1 byte
    @ or @8: operator stores value to the memory 1 byte
    $16: operator loads value from the memory 2 bytes
    @16: operator stores value to the memory 2 bytes
    $32: operator loads value from the memory 4 bytes
    @32: operator stores value to the memory 4 bytes
    $64: operator loads value from the memory 8 bytes
    @64: operator stores value to the memory 8 bytes
    2DUP: keyword to duplicate the top 2 values of the stack
    SWAP: keyword to swap the top 2 values of the stack
    DROP: keyword to drop the top value of the stack
    EXIT: keyword to end the program (calls syscall1)
    SHR: shift right bits
    SHL: shift left bits
    ORB, OR: bitwise or
    ANDB, AND: bitwise and
    DIV: integer division
    MUL: integer multiplication
    MOD: integer modulo
    OVER: swap the two values on the stack and dup the second value : a = pop() b = pop() push(b) push(a) push(b)
    !=: operator pops 2 values from the stack and push 1 if not equality and 0 otherwise
    >=: operator pops 2 values from the stack and push 1 if the first one is greater or equal than the second one and 0 otherwise
    <=: operator pops 2 values from the stack and push 1 if the first one is less or equal than the second one and 0 otherwise
    ": starts and end a string, not that for now it doesn't allow a // or a # in the string due to the fact that they are comments
    WRITE: keyword to write a string to the output file (do internally a 1 1 SYSCALL3 at each WRITE)
    MACRO: keyword to create a macro for now inlining definition of a macro is not allowed but macro inside macro is allowed except itself (recursive macro it crashes for now)
    ENDM: keyword to close a macro
    INCLUDE: keyword to include a file recursive include are managed.
    '_': single quotes to create a char (1 character allowed except for some special characters see special_chars dictionary). It's possible to print some chars like '\n' or '\t' but some issues still yet with unicode characters that are coded in more than one byte.
    VAR: keyword to create a variable followed by the name of the variable, the type of the variable
    !variable_name: assignment operator pops the value and the variable and assign the value to the variable ex: !x pop the value and assign to x.
    u8, u16, u32, u64, i8, i16, i32, i64, bool, ptr : variables types allowed for now.
    ARGC: keyword to push the number of arguments passed to the program
    ARGV: keyword to push the arguments passed to the program
    ROT: rotate the top 3 values of the stack: a b c -> b c a
    OPEN: keyword to open a file (read mode only)
    CLOSE: keyword to close a file
    OPENW: keyword to open a file (write mode only)
    READF: read content from file to a buffer
    WRITEF: write content from buffer to a file
    DIVMOD: keyword to divide and return 2 values on stack (result and reminder)
    ITOS : keyword to convert an integer to a string needs two variables one that contains the string and the second that will contains the length of the string

## Extra stack operators

MEM => DROP required. Each program that uses MEM operator needs a DROP at the end.
OVER => DROP required. Each program that uses OVER operator needs a DROP at the end.
SYSCALLx => syscalls returns the result into the stack needs to DROP if you didn't care about the result.

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

1.0.20 refactoring the error during runtime. Adding new keyword WRITE that executes internally the "1 1 SYSCALL3" instruction. It prints the string on the stdout (no need anymore to specify "string" 1 1 SYSCALL3). It's done internally.

1.0.21 refactoring the function that separates line into strings and not strings.

1.0.22 introducing macros management (not following the same rules as in the episode 8). Fixing some issue with wrong line information fixing also the write function in simulation. Removing the check of the first token of the line.

1.0.23 introducing the possibility to include files. Including char management using single quotes. Writing Fizzbuzz example.
An issue still remains with the strings management if you define some strings with different sizes it doesn't work inside a loop!
Not found why perhaps caused by OVER keyword. Probably need to review the string management later.

1.0.24 Adding standard macros for syscalls, memory 64 bits loading and storing, adding a syscall return exit code that needs now to be dropped if not used. Adding recursive include management. Includes files into "include" folder (Episode 10).

1.0.25 Adding a security loop to avoid infinite loop (limit to 10_000_000) seems to work. Adding a level information for DO loops.

1.0.26 starting variable management. Updating files to use pypy3 instead of python3. Variables should be assigned during declaration.
The non-initialized variables are not taken into account for now (segment fault during compilation).

1.0.27 fixing variable management for initialized variables and uninitialzed variables. Seems to work but need to do more tests and controls.

1.0.28 refactoring error management in porth_error.py. Changing the way to assign variables now it will be !variable_name ex !x to assign a value to the variable x. It's possible to store the result of some operators into a variable (see OPERATORS list). Adding -w flag to display warnings.

1.0.29 managing argv and argc. Adding -p flag to pass parameter to be taken in account during execution. Note that libc doesn't manage the argv by the stack but using registers (rdi for argc and rsi for argv). Adding -p flag to pass parameter to be taken in account during execution. Starting refactoring compile function.

1.0.30 refactoring compile function. Changing the way to manage argc and argv. Adding standard input management for testing ".input" extension file.

1.0.31 Managing negative numbers at compilation. Adding new operators ROT for rotating 3 elements on the stack. Adding mem operators $16, $32 for read 16, 32 bits from memory. Adding mem operators @16, @32 for write 16, 32 bits to memory. Merging all includes into std.porth easier to manage. Adding detection of stack not empty. In the stack variables declaration and values and argc, argv still remains at the end of program execution.

1.0.32 Adding OPEN and CLOSE operators to manage files. Miss some controls to avoid segmentation fault. Note that some wrong implementation can cause crash on linux (writing shared libraries, in my case libncursesw6 not working anymore lots of programs don't work anymore like gdb, nano... need to reinstall linux).

1.0.33 Adding OPENW, READF, WRITEF to have the capability to read file content and to write into a new file. Fixing README mistake between $ and @.
Missing controls on File like if open failed negative numbers return in RAX not checked.

1.0.34 Enabling warnings during test to check if the stack is empty at the end. Usage of MEM leaves address on the stack. DROP needed to keep the stack empty at the end. Probably same issue with OVER ? Adding other variables types i8, i16, i32, i64, bool and ptr. Adding controls to forbid wrong values depending the variable types. Adding ITOS keyword to convert integer to string. Needs to variable to store the result. 1st a ptr and the second the length.

## simulation

The simulation/interpreter mode is too long. By generating a shared library using cython it seems a little bit faster (I used my pytoc tool to generate the shared library). The euler6 example takes :

    time python3 porth.py -s -i examples/euler6.porth -o bin/euler6
    906609

    real    1m34.319s
    user    1m33.724s
    sys     0m0.010s

without cython:

    time python3 porth.py -s -i examples/euler6.porth -o bin/euler6
    906609

    real    2m7.769s
    user    2m7.723s
    sys     0m0.000s

the compiled version :

    time bin/euler6
    906609

    real    0m0.092s
    user    0m0.082s
    sys     0m0.009s

using pypy :

    time ./porth.py -s -i ./examples/euler6.porth -o bin/euler6
    906609

    real    0m10.606s
    user    0m10.596s
    sys     0m0.010s

link to pypy : https://www.pypy.org/download.html

## TODO

- Adding type checking to avoid invisibles bugs! like missing DROP to remove address from stack on while loops! (2 days lost of time!)
- Adding controls to check if open/read/write returns negative values.
- Adding pointers and how to dereference them ?
- Adding other types for variables (char, string, float)
- Adding controls to avoid crash on open and close operators
- Refactoring code to be simpler and more readable.
- Trying to implement similar language but using ANTLR4.
- Generate a real AST and symbol table.
- rewriting porth in porth
