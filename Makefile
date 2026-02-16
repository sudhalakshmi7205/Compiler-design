# ─── MiniCompiler Makefile ───────────────────────────────
# Convenience targets for the Python + PLY mini compiler.
# Works on Windows (with GNU Make) and Linux/macOS.
# ─────────────────────────────────────────────────────────

PYTHON  = python
SRC     = test.mini

# Install the PLY dependency
install:
	pip install -r requirements.txt

# Run the compiler on the sample program
run:
	$(PYTHON) compiler.py $(SRC)

# Run with a custom source file:  make run SRC=myfile.mini
# (The variable SRC can be overridden on the command line.)

# Assemble the generated .asm on Linux (requires NASM + ld)
assemble:
	nasm -f elf64 test.asm -o test.o
	ld test.o -o test

# Remove generated files
clean:
	-del /Q *.tac *.asm *.o parser.out parsetab.py 2>nul || true
	-rm -f  *.tac *.asm *.o parser.out parsetab.py 2>/dev/null || true

.PHONY: install run assemble clean
