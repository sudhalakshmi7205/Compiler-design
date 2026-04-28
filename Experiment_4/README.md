# Compiler Lab Tools

This project implements:

1. Removal of Left Recursion
2. Left Factoring
3. FIRST Set Computation
4. FOLLOW Set Computation

## How to Run

1. Place grammar in grammar_input.txt
2. Run:

python left_recursion.py
python left_factoring.py
python first_follow.py

## Grammar Format

Use:
# for epsilon
-> for production
| for alternatives

Example:

E -> E + T | T
T -> T * F | F
F -> ( E ) | id
