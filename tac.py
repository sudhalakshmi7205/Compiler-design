"""
tac.py — Three-Address Code (TAC) Generator
=============================================
Phase 5 of the compiler.

Walks the AST and produces a flat list of three-address instructions.

TAC instruction formats used:
    t1 = a + b          arithmetic
    t2 = 5              load constant
    x = t1              copy / assignment
    if t3 goto L1       conditional jump
    goto L2             unconditional jump
    L1:                 label
    print x             output a value
    param t1            (not used here, but shown for completeness)

Each instruction is stored as a simple string.  A more sophisticated
compiler might use tuples (op, arg1, arg2, result), but strings are
clearer for student reading.

Key concepts demonstrated:
  • Temporary variable generation (t0, t1, t2, …)
  • Label generation (L0, L1, L2, …)
  • Recursive expression flattening
  • Control-flow linearisation for if/while
"""

from ast_nodes import Program, Assign, If, While, Print, BinOp, Num, Var


class TACGenerator:
    """Generate three-address code from an AST."""

    def __init__(self):
        self.instructions = []   # list of TAC instruction strings
        self._temp_count = 0     # next temporary index
        self._label_count = 0    # next label index

    # ── Helpers ──────────────────────────────────────────────────────

    def _new_temp(self):
        """Create a fresh temporary variable name: t0, t1, …"""
        name = f"t{self._temp_count}"
        self._temp_count += 1
        return name

    def _new_label(self):
        """Create a fresh label: L0, L1, …"""
        name = f"L{self._label_count}"
        self._label_count += 1
        return name

    def _emit(self, instruction):
        """Append one TAC instruction."""
        self.instructions.append(instruction)

    # ── Public Entry Point ───────────────────────────────────────────

    def generate(self, ast):
        """Generate TAC for the full program and return the instruction list."""
        self._visit(ast)
        return self.instructions

    # ── Visitor Dispatch ─────────────────────────────────────────────

    def _visit(self, node):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise RuntimeError(f"No TAC visitor for {type(node).__name__}")
        return visitor(node)

    # ── Node Visitors ────────────────────────────────────────────────

    def _visit_Program(self, node):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_Assign(self, node):
        # Evaluate the right-hand side into a temporary (or plain value)
        rhs = self._visit(node.expr)
        self._emit(f"{node.name} = {rhs}")

    def _visit_If(self, node):
        """
        TAC pattern for if-else:

            <evaluate condition → t>
            if t goto L_then
            goto L_else            (or L_end if no else)
          L_then:
            <then body>
            goto L_end
          L_else:                  (only if else branch exists)
            <else body>
          L_end:
        """
        cond = self._visit(node.condition)

        l_then = self._new_label()
        l_else = self._new_label()
        l_end  = self._new_label()

        self._emit(f"if {cond} goto {l_then}")

        if node.else_body:
            self._emit(f"goto {l_else}")
        else:
            self._emit(f"goto {l_end}")

        self._emit(f"{l_then}:")
        for stmt in node.then_body:
            self._visit(stmt)
        self._emit(f"goto {l_end}")

        if node.else_body:
            self._emit(f"{l_else}:")
            for stmt in node.else_body:
                self._visit(stmt)

        self._emit(f"{l_end}:")

    def _visit_While(self, node):
        """
        TAC pattern for while:

          L_start:
            <evaluate condition → t>
            if t goto L_body
            goto L_end
          L_body:
            <body>
            goto L_start
          L_end:
        """
        l_start = self._new_label()
        l_body  = self._new_label()
        l_end   = self._new_label()

        self._emit(f"{l_start}:")
        cond = self._visit(node.condition)
        self._emit(f"if {cond} goto {l_body}")
        self._emit(f"goto {l_end}")

        self._emit(f"{l_body}:")
        for stmt in node.body:
            self._visit(stmt)
        self._emit(f"goto {l_start}")

        self._emit(f"{l_end}:")

    def _visit_Print(self, node):
        val = self._visit(node.expr)
        self._emit(f"print {val}")

    def _visit_BinOp(self, node):
        """
        Flatten a binary operation into temporaries:
            t1 = <left>
            t2 = <right>
            t3 = t1 <op> t2
        Returns 't3' so the caller can use it.
        """
        left  = self._visit(node.left)
        right = self._visit(node.right)
        result = self._new_temp()
        self._emit(f"{result} = {left} {node.op} {right}")
        return result

    def _visit_Num(self, node):
        """A literal number; return its string representation directly."""
        return str(node.value)

    def _visit_Var(self, node):
        """A variable reference; return its name directly."""
        return node.name


# ─── Convenience ─────────────────────────────────────────────────────

def generate_tac(ast):
    """Generate TAC for the AST and return the list of instruction strings."""
    gen = TACGenerator()
    return gen.generate(ast)


def format_tac(instructions):
    """Pretty-print the TAC list with line numbers."""
    lines = ["\nThree-Address Code (TAC)", '-' * 45]
    for i, instr in enumerate(instructions):
        # Labels are not indented; all others are.
        if instr.endswith(':'):
            lines.append(f"  {instr}")
        else:
            lines.append(f"    {i:>3}:  {instr}")
    lines.append('-' * 45)
    return '\n'.join(lines)
