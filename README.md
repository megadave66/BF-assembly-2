# BF assembly 2
----------------

**Intro**
-------------
*This is a rewrite of the the project [BF assembly](https://github.com/megadave66/BF-assembly).*
This is an assembly language that compiles into brainf**ck, a very popular but hard-to-use esoteric language (Esolang). The assembler is written in Python, a very high-level and easy-to-use programming language.

**Timeline**
---------------
1. Installing and using the compiler
2. Basics of BF assembly
3. Controll flow
4. Macros
5. Standard library

**Part 1: Installing and using the compiler**
-----------------------
*IMPORTANT: If you haven't done so, download python on your computer before continuing.*

Start by downloading `assembler.py` from the repo and move it into an empty folder. Then in that folder, create a file called `main.txt` *(The .txt isn't nessesary, you can use any file format like .asm, .bf, etc.)* and type in the following:

```bf assembly
rt 1
lt 1
inc 1
print
```
Then run `assembler.py` and enter the code file *(`main.txt`)* and the file where you want to store the output brainf**ck code:
```terminal
Enter code file: main.txt
Enter output brainf**ck code file: output.txt
Compiled to output.txt!
```
After doing that, open up `output.txt` and you should see the following:
```brainf**ck
><+.
```
If you do, then well done, you can advance to Part 2. But if not, compare the code given here with the code on your computer.

**Part 2: Basics of BF assembly**
---------------------------
*IMPORTANT: This part assumes that you have previous knowlege of how brainf\*ck works.*

Before we explain the commands, you should know that we will represent parameters as `$`, then the index of the parameter. *(Zero-indexed)* So the first parameter will be represented as `$0`, the second as `$1`, and so on.

You should also know that comments start with the `;` character. Now let's take a look at how you actually write code.

These are the basic instructions of BF assembly:
- `rt`: Moves The memory cursor `$0` cells to the right
- `lt`: Moves The memory cursor `$0` cells to the left
- `inc`: Increases the current memory cell by `$0`
- `dec`: Decreases the current memory cell by `$0`
- `inp`: Sets the current cell to a user-inputted number
- `print`: Prints the value of the current memory cell

Example:

```BF assembly
; Program that takes in two numbers, adds 3 to both, and then outputs them

; Accept two input values
inp
rt 1
inp

; Add three to both
inc 3
lt 1
inc 3

; Output the two (new) numbers
print
rt 1
print
```
**TIP: If your number starts with `#`, it will be accepted as a hexadecimal number.**

**Part 3: Controll flow**
---------------------------
To replicate the [] loop in BF assembly, start by writing `.loop` *(This is equivalent to the command `[`)* and then `.endloop`. *(This is equivalent to the command `]`)* Then, what you write in between those two will be inside the loop.

Example:

```BF assembly
; Program to accept two values and output their sum

inp
rt 1
inp
lt 1

.loop
    dec 1
    rt 1
    inc 1
    lt 1
.endloop

rt 1
print
```

If your repeates itself, like this:

```BF assembly
inp
rt 1
inp
rt 1
inp
rt 1
inp
rt 1
inp
rt 1
```

You can shorten it, using the instruction `.rp [Number of times]`.

Example:
```BF assembly
.rp 5
    inp
    rt 1
.endrp
```

**Part 4: Macros**
---------------------
Macros are used to add more abstraction to your code. They are useful if you have code that repeats itself a lot.

When we use macros, we specify the parameters as we did in Part 3.

Example:

```BF assembly
; Move the cursor 2 cells right and 1 cell left $0 times
.macro 2_rt_1_lt
    .rp $0
        rt 2
        lt 1
    .endrp
.endmacro

2rt1lt 5
```
They can be useful if you have code that can be abstracted away:
```BF assembly
.macro set_current_to_0
    .loop
        dec 1
    .endloop
.endloop

inp
print
set_current_to_0
print
; Output [Whatever the user inputs], 0
```
If you have to many macros for a single code file, you can put those other macros in a library.

Example:

`library.txt`
```BF assembly
.macro set_current_to_0
    .loop
        dec 1
    .endloop
.endloop
```
`main.txt`
```BF assembly
include library.txt

inp
print
set_current_to_0
print
```

**Part 4: Standard library**
-----------------------
The standard library is a library built-into `assembler.py`, and implements a wide range of macros:
- `set_zero`: Sets current memory cell to `0`
- `set`: Sets current memory cell to `$0`
- `push_lt`: Moves the current value of the cell `$0` cells to the left
- `push_rt`: Moves the current value of the cell `$0` cells to the right
- `mult_lt`: Multiplies the value of the current memory vell by `$0` and save the value to the cell `$1` cells to the left
- `mult_rt`: Multiplies the value of the current memory vell by `$0` and save the value to the cell `$1` cells to the right
- `get_multiple_inputs`: Take `$0` values of user input (Goes to the first value when done)
- `say_multiple_values`: Say the first `$0` values *(Including the current one)* to the right *(Goes back to the first value when done)*

*NOTE: the language is still in it's beta phase and contributions to the standard library would be encouraged.*

**Part 5: Importing files**
---------------------
If you want to import a file of numbers into BF assembly, you can use the `load` instruction.

Example:

`numbers.txt`
```text
1
2
3
4
```
`main.txt`
```BF assembly
load numbers.txt
lt 4
say_multiple_values 4
```

*NOTE: after running the `load` command, the memory cursor will be 1 cell in front of the last value.*
