"""
symbol_table.py — Symbol Table
================================
Phase 3 of the compiler.

The symbol table records every variable that appears in the source
program.  It stores:
    • name  — the identifier string
    • type  — data type (always 'int' in our mini-language)
    • scope — which scope the variable belongs to ('global' here)

The semantic analyser populates this table during its tree walk, and
later phases (TAC, codegen) query it.

Key concepts demonstrated:
  • Dictionary-based symbol storage
  • declare / lookup / contains helpers
  • Pretty-print dump for debugging
"""


class SymbolTable:
    """
    A simple, single-scope symbol table backed by a Python dict.

    Extending to multiple scopes (e.g. for functions) would involve
    chaining SymbolTable objects or keeping a scope stack.
    """

    def __init__(self):
        # Internal storage:  name → { 'type': str, 'scope': str }
        self._symbols = {}

    # ── Core Operations ──────────────────────────────────────────────

    def declare(self, name, var_type='int', scope='global'):
        """
        Register a new variable.  If it already exists we silently
        update its type (useful for our simple language where the first
        assignment is the declaration).
        """
        self._symbols[name] = {
            'type':  var_type,
            'scope': scope,
        }

    def lookup(self, name):
        """
        Return the symbol-table entry for *name*, or None if the
        variable has not been declared.
        """
        return self._symbols.get(name)

    def contains(self, name):
        """Check whether *name* has been declared."""
        return name in self._symbols

    # ── Utility ──────────────────────────────────────────────────────

    def all_symbols(self):
        """Return a copy of the internal dict (read-only view)."""
        return dict(self._symbols)

    def dump(self):
        """
        Pretty-print the symbol table.
        Example output:
            Symbol Table
            ─────────────────────────────────────
            Name         Type    Scope
            ─────────────────────────────────────
            x            int     global
            total        int     global
        """
        line = '-' * 45
        rows = [
            f"\n{'Symbol Table':^45}",
            line,
            f"{'Name':<15} {'Type':<10} {'Scope':<10}",
            line,
        ]
        for name, info in self._symbols.items():
            rows.append(f"{name:<15} {info['type']:<10} {info['scope']:<10}")
        rows.append(line)
        return '\n'.join(rows)

    def __repr__(self):
        return f"SymbolTable({self._symbols})"
