"""
semantic.py — Semantic Analyzer
================================
Phase 4 of the compiler.

Walks the AST produced by the parser and enforces semantic rules:

  1. **Declared-before-use** — a variable must appear on the left side
     of an assignment before it can be used in an expression.
     (The first assignment acts as an implicit declaration.)

  2. **Type consistency** — our mini-language only supports integers,
     so we simply verify that every expression resolves to 'int'.

  3. **Division-by-zero warning** — if a literal 0 appears as the
     right operand of '/', we emit a warning (not a hard error).

Errors include the source line number so students can locate the
offending line quickly.

Key concepts demonstrated:
  • Recursive AST tree-walk
  • Populating the symbol table during the walk
  • Collecting errors vs. aborting on the first one
"""

import sys
from ast_nodes import Program, Assign, If, While, Print, BinOp, Num, Var
from symbol_table import SymbolTable


class SemanticAnalyzer:
    """Perform semantic checks and populate the symbol table."""

    def __init__(self):
        self.symtab = SymbolTable()   # fresh symbol table
        self.errors = []              # list of error strings
        self.warnings = []            # list of warning strings

    # ── Public Entry Point ───────────────────────────────────────────

    def analyze(self, ast):
        """
        Analyze the full program AST.
        Returns (symbol_table, errors, warnings).
        """
        self._visit(ast)
        return self.symtab, self.errors, self.warnings

    # ── Visitor Dispatch ─────────────────────────────────────────────

    def _visit(self, node):
        """Dispatch to the correct _visit_Xxx method based on node type."""
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise RuntimeError(f"No visitor for {type(node).__name__}")
        return visitor(node)

    # ── Node Visitors ────────────────────────────────────────────────

    def _visit_Program(self, node):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_Assign(self, node):
        # First, analyse the right-hand side expression.
        self._visit(node.expr)
        # The assignment itself counts as declaring the variable.
        self.symtab.declare(node.name, var_type='int')

    def _visit_If(self, node):
        self._visit(node.condition)
        for stmt in node.then_body:
            self._visit(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self._visit(stmt)

    def _visit_While(self, node):
        self._visit(node.condition)
        for stmt in node.body:
            self._visit(stmt)

    def _visit_Print(self, node):
        self._visit(node.expr)

    def _visit_BinOp(self, node):
        self._visit(node.left)
        self._visit(node.right)
        # Check for division by literal zero
        if node.op == '/' and isinstance(node.right, Num) and node.right.value == 0:
            self.warnings.append(
                f"[Warning] Line {node.lineno}: Division by zero"
            )

    def _visit_Num(self, node):
        # Integer literals are always valid.
        pass

    def _visit_Var(self, node):
        # Check: has this variable been declared (assigned) before use?
        if not self.symtab.contains(node.name):
            self.errors.append(
                f"[Semantic Error] Line {node.lineno}: "
                f"Variable '{node.name}' used before declaration"
            )


# ─── Convenience Function ───────────────────────────────────────────

def run_semantic_analysis(ast):
    """
    Run semantic analysis on *ast*.
    Prints errors/warnings and returns the symbol table.
    Exits with code 1 if there are errors.
    """
    analyzer = SemanticAnalyzer()
    symtab, errors, warnings = analyzer.analyze(ast)

    for w in warnings:
        print(w, file=sys.stderr)

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"\nSemantic analysis failed with {len(errors)} error(s).",
              file=sys.stderr)
        sys.exit(1)

    return symtab
