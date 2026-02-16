"""
ast_nodes.py — Abstract Syntax Tree (AST) Node Definitions
===========================================================
The parser builds a tree of these nodes.  Every later phase
(semantic analysis, TAC generation, code generation) walks this tree.

Each class represents one language construct:
  Program   → the whole source file (list of statements)
  Assign    → variable = expression
  If        → if (cond) { … } else { … }
  While     → while (cond) { … }
  Print     → print(variable)
  BinOp     → left op right   (arithmetic / comparison)
  Num       → integer literal
  Var       → variable reference
"""


# ─── Program ────────────────────────────────────────────────────────
class Program:
    """Root node — holds the entire list of statements."""
    def __init__(self, statements):
        self.statements = statements          # list[Statement]

    def __repr__(self):
        return f"Program({self.statements})"


# ─── Statements ─────────────────────────────────────────────────────
class Assign:
    """Assignment: <name> = <expr> ;"""
    def __init__(self, name, expr, lineno=0):
        self.name = name      # str — variable name
        self.expr = expr      # expression node
        self.lineno = lineno  # source line (for error messages)

    def __repr__(self):
        return f"Assign({self.name}, {self.expr})"


class If:
    """If-else: if (<cond>) { <then_body> } else { <else_body> }"""
    def __init__(self, condition, then_body, else_body=None, lineno=0):
        self.condition = condition    # expression node (comparison)
        self.then_body = then_body    # list[Statement]
        self.else_body = else_body    # list[Statement] or None
        self.lineno = lineno

    def __repr__(self):
        return f"If({self.condition}, then={self.then_body}, else={self.else_body})"


class While:
    """While loop: while (<cond>) { <body> }"""
    def __init__(self, condition, body, lineno=0):
        self.condition = condition    # expression node
        self.body = body              # list[Statement]
        self.lineno = lineno

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class Print:
    """Print statement: print(<expr>) ;"""
    def __init__(self, expr, lineno=0):
        self.expr = expr              # expression node
        self.lineno = lineno

    def __repr__(self):
        return f"Print({self.expr})"


# ─── Expressions ────────────────────────────────────────────────────
class BinOp:
    """Binary operation: <left> <op> <right>
       op is one of: +  -  *  /  ==  !=  <  >  <=  >=
    """
    def __init__(self, left, op, right, lineno=0):
        self.left = left      # expression node
        self.op = op          # str — operator symbol
        self.right = right    # expression node
        self.lineno = lineno

    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"


class Num:
    """Integer literal, e.g. 42"""
    def __init__(self, value, lineno=0):
        self.value = value    # int
        self.lineno = lineno

    def __repr__(self):
        return f"Num({self.value})"


class Var:
    """Variable reference, e.g. x"""
    def __init__(self, name, lineno=0):
        self.name = name      # str
        self.lineno = lineno

    def __repr__(self):
        return f"Var({self.name})"
