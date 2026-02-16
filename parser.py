"""
parser.py — Syntax Analyzer (Parser)
======================================
Phase 2 of the compiler.

Uses PLY's yacc module to build an Abstract Syntax Tree (AST) from
the token stream produced by the lexer.

Grammar (informally):
    program      → statement_list
    statement    → assignment | if_stmt | while_stmt | print_stmt
    assignment   → ID '=' expression ';'
    if_stmt      → 'if' '(' expression ')' block
                  | 'if' '(' expression ')' block 'else' block
    while_stmt   → 'while' '(' expression ')' block
    print_stmt   → 'print' '(' expression ')' ';'
    block        → '{' statement_list '}'
    expression   → expression op expression | '(' expression ')' | NUMBER | ID
    op           → + | - | * | / | == | != | < | > | <= | >=

Key concepts demonstrated:
  • Operator precedence & associativity (precedence tuple)
  • Building AST nodes inside grammar actions
  • Error recovery with p_error
"""

import ply.yacc as yacc
import sys

# Import the token list from our lexer (PLY requires this).
from lexer import tokens          # noqa: F401  — PLY introspects this list

# Import AST node classes so grammar actions can build the tree.
from ast_nodes import (
    Program, Assign, If, While, Print, BinOp, Num, Var
)


# ─── Operator Precedence (lowest → highest) ─────────────────────────
# PLY resolves shift/reduce conflicts using this table.
# 'left' means left-associative:  a - b - c  ⟹  (a-b) - c

precedence = (
    ('left', 'EQ', 'NEQ'),             # ==  !=
    ('left', 'LT', 'GT', 'LE', 'GE'),  # <  >  <=  >=
    ('left', 'PLUS', 'MINUS'),          # +  -
    ('left', 'TIMES', 'DIVIDE'),        # *  /
)


# ─── Grammar Rules ──────────────────────────────────────────────────
# Each function p_xxx defines one production.
# p[0] is the left-hand side; p[1], p[2], … are the right-hand symbols.

def p_program(p):
    """program : statement_list"""
    p[0] = Program(p[1])


# statement_list builds a Python list of statements.
def p_statement_list(p):
    """statement_list : statement_list statement
                      | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]     # append new statement
    else:
        p[0] = [p[1]]            # first statement → new list


# ── Assignment ──
def p_statement_assign(p):
    """statement : ID ASSIGN expression SEMI"""
    p[0] = Assign(name=p[1], expr=p[3], lineno=p.lineno(1))


# ── If / If-Else ──
def p_statement_if(p):
    """statement : IF LPAREN expression RPAREN block"""
    p[0] = If(condition=p[3], then_body=p[5], lineno=p.lineno(1))


def p_statement_if_else(p):
    """statement : IF LPAREN expression RPAREN block ELSE block"""
    p[0] = If(condition=p[3], then_body=p[5],
              else_body=p[7], lineno=p.lineno(1))


# ── While ──
def p_statement_while(p):
    """statement : WHILE LPAREN expression RPAREN block"""
    p[0] = While(condition=p[3], body=p[5], lineno=p.lineno(1))


# ── Print ──
def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN SEMI"""
    p[0] = Print(expr=p[3], lineno=p.lineno(1))


# ── Block ──
def p_block(p):
    """block : LBRACE statement_list RBRACE"""
    p[0] = p[2]                   # just return the list of statements


def p_block_empty(p):
    """block : LBRACE RBRACE"""
    p[0] = []                     # empty block


# ── Expressions ──────────────────────────────────────────────────────

def p_expression_binop(p):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression
                  | expression EQ     expression
                  | expression NEQ    expression
                  | expression LT     expression
                  | expression GT     expression
                  | expression LE     expression
                  | expression GE     expression"""
    p[0] = BinOp(left=p[1], op=p[2], right=p[3], lineno=p.lineno(2))


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]                   # parentheses just pass through


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = Num(value=p[1], lineno=p.lineno(1))


def p_expression_id(p):
    """expression : ID"""
    p[0] = Var(name=p[1], lineno=p.lineno(1))


# ─── Error Handling ──────────────────────────────────────────────────
def p_error(p):
    """Called by PLY when the parser encounters a syntax error."""
    if p:
        print(f"[Syntax Error] Unexpected token '{p.value}' ({p.type}) "
              f"at line {p.lineno}", file=sys.stderr)
    else:
        print("[Syntax Error] Unexpected end of input", file=sys.stderr)
    sys.exit(1)


# ─── Build the Parser ───────────────────────────────────────────────
# write_tables=False avoids creating parser.out/parsetab.py clutter.
parser = yacc.yacc(write_tables=False, debug=False)


def parse(source_code):
    """Parse source code string and return the AST (a Program node)."""
    from lexer import lexer as lex_instance
    lex_instance.lineno = 1       # reset lexer line counter
    return parser.parse(source_code, lexer=lex_instance)
