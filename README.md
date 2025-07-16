# Two-Pass Assembler for Custom 16-bit CPU

This project implements a fully functional two-pass assembler for a custom 16-bit RISC-style CPU (from Project 7). The assembler translates human-readable assembly language into machine code compatible with our CPU’s architecture and instruction set. It is written in Python and tested extensively on various programs, including loops, recursion, and interactive input/output.

## Assembler Architecture

The assembler operates in two main phases:

### **Pass 1: Label Resolution**
- Tokenizes the input `.txt` file, removing whitespace and comments.
- Constructs a list of tokenized instructions.
- Maps all labels to their corresponding instruction addresses (line numbers).
- Produces a cleaned version of the program (without labels) and a label-address dictionary.

### **Pass 2: Machine Code Generation**
- Reprocesses the cleaned token stream.
- Converts each instruction and its operands into 16-bit machine code using the label dictionary when needed.
- Outputs `.mif` files ready for ROM initialization on the CPU.

## Programs Assembled & Simulated

### **1. Test Program**
A sample program verifying basic MOVEI, BRA, and BRAZ operations. Used to confirm assembler correctness.

### **2. Fibonacci Generator**
Generates the first 10 numbers of the Fibonacci sequence using iterative looping with registers and branches.  
- RA and RB initialized to 0 and 1  
- RC used as a countdown counter  
- Each result stored in the output port  
- **Result visible in `FibonacciGTK.png`**

### **3. Recursive SumN**
Computes the sum of numbers from 1 to 10 using recursion and condition-based branching.  
- RA accumulates result  
- RB initialized to 10 (N), RC to 1  
- Recursive call made until RB = 0  
- Output: 55 (`0x37`) confirmed in `Recursive.png`

### **4. Number Guessing Game**
A simple game where:
- The secret number is hardcoded into a register.
- User guesses via the input port.
- Feedback:
  - `0` for correct
  - `1` if too low
  - `2` if too high  
- Uses conditional branching and subtraction for comparison.  
- Fully tested and demonstrated in `Game.mp4`

## Extensions

- **Clock Slowing & Decimal Output**  
  Enhanced hardware output with slower clock and bin-to-decimal display from earlier projects. Enabled visual feedback for Fibonacci and recursive functions.

- **Interactive Game via Assembly**  
  Pushed instruction set to support a mini-game, showing that even simple RISC CPUs can perform interactive tasks under constrained logic.

## File Structure

- **Project/**
  - `assembler.py` – The two-pass assembler.
  - `*.txt` – Input assembly programs.
  - `*.mif` – Output machine code files.
  - `*.vhd` – CPU, ALU, RAM, and ROM designs.
  - `*.png` – GTKWave visualizations and display outputs.
  - `*.mp4` – Demonstration videos for Fibonacci, SumN, and Game programs.

- **Project8_Report_AayanShah.pdf**  
  Full report with implementation details, testing walkthrough, and analysis.

## Acknowledgements

Thanks to Maya, Azam, Aleksandra, Muneeb, and Manish for support in testing and debugging. Deep appreciation to our professors and TAs for guidance throughout the course. Online forums and documentation also played a key role in shaping the assembler's structure.

## Author

**Aayan Shah**  
Computer Science & Physics Student  
[GitHub Profile](https://github.com/aayans314)
