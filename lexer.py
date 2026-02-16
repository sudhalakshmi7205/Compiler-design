"""
lexer.py — Lexical Analyzer (Scanner)
======================================
Phase 1 of the compiler.

Uses the PLY (Python Lex-Yacc) library to convert raw source text
into a stream of *tokens*.  Each token has:
    type   – e.g. 'NUMBER', 'ID', 'PLUS'
    value  – the actual text / converted value
    lineno – source line number (for error reporting)

Key concepts demonstrated:
  • Reserved-word handling via a dictionary
  • Regular-expression token rules (simple and function-based)
  • Line-number tracking with t_newline
  • Illegal-character error reporting
"""

import ply.lex as lex
import sys


# ─── Reserved Words ─────────────────────────────────────────────────
# PLY convention: map the source text → token type.
# This lets us recognise keywords without a separate rule for each one.

reserved = {
    'if':    'IF',
    'else':  'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
}


# ─── Token List ─────────────────────────────────────────────────────
# PLY requires a module-level list called `tokens`.

tokens = [
    # Literals
    'NUMBER',          # integer literal   e.g. 42
    'ID',              # identifier        e.g. myVar

    # Arithmetic operators
    'PLUS',            # +
    'MINUS',           # -
    'TIMES',           # *
    'DIVIDE',          # /

    # Assignment
    'ASSIGN',          # =

    # Comparison operators
    'EQ',              # ==
    'NEQ',             # !=
    'LT',              # <
    'GT',              # >
    'LE',              # <=
    'GE',              # >=

    # Delimiters
    'SEMI',            # ;
    'LPAREN',          # (
    'RPAREN',          # )
    'LBRACE',          # {
    'RBRACE',          # }
] + list(reserved.values())   # add IF, ELSE, WHILE, PRINT


# ─── Simple Token Rules (single regex string) ───────────────────────
# PLY matches these strings LONGEST FIRST, so  '=='  is tried before '='.

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_SEMI    = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

# Comparison / assignment — ORDER MATTERS for multi-char operators.
t_EQ      = r'=='
t_NEQ     = r'!='
t_LE      = r'<='
t_GE      = r'>='
t_LT      = r'<'
t_GT      = r'>'
t_ASSIGN  = r'='


# ─── Function-Based Token Rules ─────────────────────────────────────
# These need a function so we can transform the value or do look-ups.

def t_NUMBER(t):
    r'\d+'                          # one or more digits
    t.value = int(t.value)          # convert string → int
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'      # letters/underscore, then alnum
    # Check if the identifier is actually a reserved keyword
    t.type = reserved.get(t.value, 'ID')
    return t


# ─── Ignored Characters ─────────────────────────────────────────────
# Spaces and tabs are skipped silently.
t_ignore = ' \t'


# ─── Comments (// single-line) ──────────────────────────────────────
def t_COMMENT(t):
    r'//[^\n]*'                     # everything after // until newline
    pass                            # discard — do not return a token


# ─── Newlines (for line-number tracking) ────────────────────────────
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # count how many newlines we saw


# ─── Error Handling ──────────────────────────────────────────────────
def t_error(t):
    """Called when the lexer encounters a character it cannot match."""
    print(f"[Lexer Error] Illegal character '{t.value[0]}' at line {t.lineno}",
          file=sys.stderr)
    t.lexer.skip(1)                 # skip one char and keep going


# ─── Build the Lexer ────────────────────────────────────────────────
lexer = lex.lex()


def tokenize(source_code):
    """
    Tokenize the given source string and return a list of tokens.
    Each token is a (type, value, lineno) tuple — handy for display.
    """
    lexer.input(source_code)
    lexer.lineno = 1                # reset line counter
    token_list = []
    while True:
        tok = lexer.token()
        if tok is None:
            break
        token_list.append((tok.type, tok.value, tok.lineno))
    return token_list
