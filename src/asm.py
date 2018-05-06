#!/usr/bin/env python3

from parser import Parser
from visitors import AssemblyVisitor

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    par = Parser()

    if len(args) == 2:
        with open(args[0], "r") as source, \
                open(args[1], "wb") as destination:
            text = source.read() + "\0"
            ast = par.parse(text)
            asm = ast.accept(AssemblyVisitor)
            destination.write(asm)
    else:
        print("Usage: ./asm.py [input] [output]")
