# MiniCompiler — A Complete Mini Compiler in Python + PLY

A **fully working compiler** that takes a small imperative language through **all six compiler phases**:

| # | Phase | File |
|---|-------|------|
| 1 | Lexical Analysis | `lexer.py` |
| 2 | Syntax Analysis (Parsing) | `parser.py` |
| 3 | Symbol Table | `symbol_table.py` |
| 4 | Semantic Analysis | `semantic.py` |
| 5 | Three-Address Code (TAC) | `tac.py` |
| 6 | x86-64 Code Generation | `codegen.py` |

**Driver**: `compiler.py` — orchestrates everything and prints phase-by-phase output.

---

## Source Language Features

```
// Variables & arithmetic
x = 10;
y = x + 5 * 2;

// If-else
if (x > y) {
    z = x;
} else {
    z = y;
}

// While loop
i = 0;
while (i < 10) {
    i = i + 1;
}

// Print
print(z);
```

Supported operators: `+  -  *  /  ==  !=  <  >  <=  >=`
Single-line comments: `// comment`

---

## Quick Start

### 1. Prerequisites

- **Python 3.7+** (check with `python --version`)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs [PLY](https://www.dabeaz.com/ply/) (Python Lex-Yacc).

### 3. Run the compiler

```bash
python compiler.py test.mini
```

### 4. What you'll see

The compiler prints the output of **every phase**:

1. **Token list** — each token with type, value, line number
2. **AST** — indented tree showing the program structure
3. **Semantic check result** — pass/fail + symbol table
4. **Three-Address Code** — flat intermediate representation
5. **x86-64 Assembly** — NASM syntax, ready for assembly
6. **Output files** — `test.tac` and `test.asm` are written to disk

### 5. (Optional) Assemble and run on Linux

```bash
nasm -f elf64 test.asm -o test.o
ld test.o -o test
./test
```

---

## Project Structure

```
compiler design/
├── ast_nodes.py       # AST node class definitions
├── lexer.py           # Phase 1: Lexical Analyzer (PLY lex)
├── parser.py          # Phase 2: Syntax Analyzer  (PLY yacc)
├── symbol_table.py    # Phase 3: Symbol Table
├── semantic.py        # Phase 4: Semantic Analyzer
├── tac.py             # Phase 5: Three-Address Code generator
├── codegen.py         # Phase 6: x86-64 NASM code generator
├── compiler.py        # Main driver (runs all phases)
├── test.mini          # Sample input program
├── requirements.txt   # Python dependencies (ply)
├── Makefile           # Convenience targets
└── README.md          # This file
```

---

## How Each Phase Works

### Phase 1 — Lexical Analysis (`lexer.py`)
Converts raw source text into tokens using regular expressions.
Tracks line numbers for error messages. Handles reserved words
(`if`, `else`, `while`, `print`) and single-line comments.

### Phase 2 — Syntax Analysis (`parser.py`)
Uses a context-free grammar with operator precedence to build an
Abstract Syntax Tree (AST). Reports syntax errors with line numbers.

### Phase 3 — Symbol Table (`symbol_table.py`)
A dictionary-based table that records every variable's name, type,
and scope. Populated during semantic analysis.

### Phase 4 — Semantic Analysis (`semantic.py`)
Tree-walks the AST to check:
- Variable must be assigned before use
- Type consistency (all `int`)
- Division-by-zero warnings

### Phase 5 — TAC Generation (`tac.py`)
Flattens the AST into a linear list of three-address instructions:
```
t0 = y * 2
t1 = x + t0
z = t1
```

### Phase 6 — Code Generation (`codegen.py`)
Translates TAC into x86-64 NASM assembly. Variables live on the
stack. Includes a `print_int` subroutine for output.

---

## Error Handling Examples

**Undeclared variable:**
```
b = a + 1;    // ERROR if 'a' not assigned before this line
```
Output:
```
[Semantic Error] Line 1: Variable 'a' used before declaration
```

**Syntax error:**
```
x = 10 +;     // missing right operand
```
Output:
```
[Syntax Error] Unexpected token ';' (SEMI) at line 1
```

**Illegal character:**
```
x = 10 @ 5;
```
Output:
```
[Lexer Error] Illegal character '@' at line 1
```

---

## Using with Make (optional)

```bash
make install     # pip install ply
make run         # python compiler.py test.mini
make clean       # remove generated .tac, .asm, etc.
```

Override the source file:
```bash
make run SRC=myprogram.mini
```

---

## License

This project is for educational purposes — free to use, modify, and submit.
