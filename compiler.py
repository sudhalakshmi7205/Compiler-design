"""
compiler.py -- Main Driver
===========================
Orchestrates ALL six compiler phases and pretty-prints the output
of each stage so students can see exactly what happens at every step.

Usage:
    python compiler.py <source_file.mini>

Phases executed in order:
  1. Lexical Analysis   -> token list
  2. Syntax Analysis    -> AST
  3. Semantic Analysis  -> symbol table (+ error checking)
  4. TAC Generation     -> three-address code listing
  5. Code Generation    -> x86-64 NASM assembly
  6. Output files       -> <name>.tac  and  <name>.asm
"""

import sys
import os


def banner(title):
    """Print a prominent phase heading."""
    width = 55
    print()
    print('=' * width)
    print(f"  Phase: {title}")
    print('=' * width)


def main():
    # -- Check command-line arguments ------------------------------------
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file.mini>", file=sys.stderr)
        sys.exit(1)

    source_file = sys.argv[1]

    if not os.path.isfile(source_file):
        print(f"Error: file '{source_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Read source code
    with open(source_file, 'r') as f:
        source_code = f.read()

    print(f"\n[*] Compiling: {source_file}")
    print(f"    Source length: {len(source_code)} characters")

    # -- Phase 1: Lexical Analysis ---------------------------------------
    banner("1 - Lexical Analysis (Tokenisation)")

    from lexer import tokenize
    tokens = tokenize(source_code)

    print(f"  Tokens generated: {len(tokens)}\n")
    print(f"  {'Type':<12} {'Value':<15} {'Line':>4}")
    print(f"  {'---'*4:<12} {'---'*5:<15} {'---':>4}")
    for ttype, tval, tline in tokens:
        print(f"  {ttype:<12} {str(tval):<15} {tline:>4}")

    # -- Phase 2: Syntax Analysis (Parsing -> AST) -----------------------
    banner("2 - Syntax Analysis (Parsing)")

    from parser import parse
    ast = parse(source_code)

    # Pretty-print the AST with indentation
    def pp_ast(node, indent=0):
        """Recursively pretty-print an AST node."""
        prefix = '  ' + '  ' * indent
        from ast_nodes import (Program, Assign, If, While,
                                Print as PrintNode, BinOp, Num, Var)
        if isinstance(node, Program):
            print(f"{prefix}Program")
            for s in node.statements:
                pp_ast(s, indent + 1)
        elif isinstance(node, Assign):
            print(f"{prefix}Assign  {node.name} =")
            pp_ast(node.expr, indent + 1)
        elif isinstance(node, If):
            print(f"{prefix}If")
            print(f"{prefix}  condition:")
            pp_ast(node.condition, indent + 2)
            print(f"{prefix}  then:")
            for s in node.then_body:
                pp_ast(s, indent + 2)
            if node.else_body:
                print(f"{prefix}  else:")
                for s in node.else_body:
                    pp_ast(s, indent + 2)
        elif isinstance(node, While):
            print(f"{prefix}While")
            print(f"{prefix}  condition:")
            pp_ast(node.condition, indent + 2)
            print(f"{prefix}  body:")
            for s in node.body:
                pp_ast(s, indent + 2)
        elif isinstance(node, PrintNode):
            print(f"{prefix}Print")
            pp_ast(node.expr, indent + 1)
        elif isinstance(node, BinOp):
            print(f"{prefix}BinOp '{node.op}'")
            pp_ast(node.left, indent + 1)
            pp_ast(node.right, indent + 1)
        elif isinstance(node, Num):
            print(f"{prefix}Num({node.value})")
        elif isinstance(node, Var):
            print(f"{prefix}Var({node.name})")

    pp_ast(ast)

    # -- Phase 3 & 4: Semantic Analysis + Symbol Table -------------------
    banner("3 - Semantic Analysis & Symbol Table")

    from semantic import run_semantic_analysis
    symtab = run_semantic_analysis(ast)

    print("  [OK] Semantic analysis passed -- no errors.")
    print(symtab.dump())

    # -- Phase 5: Three-Address Code Generation --------------------------
    banner("4 - Three-Address Code (TAC) Generation")

    from tac import generate_tac, format_tac
    tac_instructions = generate_tac(ast)
    print(format_tac(tac_instructions))

    # -- Phase 6: x86-64 Assembly Code Generation ------------------------
    banner("5 - x86-64 Assembly Code Generation (NASM)")

    from codegen import generate_assembly
    asm_code = generate_assembly(tac_instructions, symtab)

    # Print first 60 lines as a preview
    asm_lines = asm_code.strip().split('\n')
    for line in asm_lines[:60]:
        print(f"  {line}")
    if len(asm_lines) > 60:
        print(f"  ... ({len(asm_lines) - 60} more lines)")

    # -- Write Output Files ----------------------------------------------
    banner("6 - Writing Output Files")

    base_name = os.path.splitext(source_file)[0]
    tac_file = base_name + '.tac'
    asm_file = base_name + '.asm'

    with open(tac_file, 'w') as f:
        f.write('\n'.join(tac_instructions) + '\n')
    print(f"  -> TAC written to:      {tac_file}")

    with open(asm_file, 'w') as f:
        f.write(asm_code)
    print(f"  -> Assembly written to: {asm_file}")

    print()
    print("=" * 55)
    print("  [OK] Compilation complete!")
    print("=" * 55)
    print()
    print("  To assemble and run on Linux (x86-64):")
    print(f"    nasm -f elf64 {asm_file} -o {base_name}.o")
    print(f"    ld {base_name}.o -o {base_name}")
    print(f"    ./{base_name}")
    print()


if __name__ == '__main__':
    main()
