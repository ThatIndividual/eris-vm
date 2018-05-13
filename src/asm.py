#!/usr/bin/env python3
from assembler import AssemblerVisitor
from parser import Parser
from printer import PrintVisitor
from resolver import ResolverVisitor

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    par = Parser()

    if len(args) == 2:
        with open(args[0], "r") as source, \
                open(args[1], "wb") as destination:
            text = source.read() + "\0"
            ast = par.parse(text)
            ast.accept(ResolverVisitor())
            print(ast.accept(PrintVisitor))
            asm = ast.accept(AssemblerVisitor())
            destination.write(asm)
    else:
        print("Usage: ./asm.py [input] [output]")
