from typing import List

from ast import Section, I32Ins, AddIns, SubIns, MulIns, DivIns, PrintIns, I32Cons, ProgramAst, Register
from lexer import Lexer, Tok


class ParserError(Exception):
    pass


class Parser:
    def __init__(self):
        self.lex = Lexer()
        self.path = None
        self.prev_tok = None
        self.this_tok = None

    def parse(self, text):
        self.lex.feed(text)
        self.tok_next()
        return self.program()

    def program(self):
        # program -> section* "EOF"
        sections = []
        while not self.tok_is([Tok.EOF]):
            sections.append(self.section())
        return ProgramAst(sections)

    def section(self):
        # section -> section identifier do
        #                instruction*
        #            end
        self.tok_consume(Tok.SECTION, "Expected the beginning of a section")
        self.tok_consume(Tok.ID,
                         "A section name should follow the `section` keyword")
        id = self.prev_tok
        self.tok_consume(Tok.DO,
                         "Expected a `do ... end` block after section definition")
        ins = []
        while not self.tok_is([Tok.END, Tok.EOF]):
            ins.append(self.ins())
        self.tok_consume(Tok.END, "Missing `end` keyword after block")
        return Section(id, ins)

    def ins(self):
        # instructions -> i32_ins
        #      | add_ins
        #      | sub_ins
        #      | mul_ins
        #      | div_ins
        #      | print_ins
        if self.tok_matches(Tok.I32_INS):
            return self.i32_ins()
        elif self.tok_matches(Tok.ADD_INS):
            return self.add_ins()
        elif self.tok_matches(Tok.SUB_INS):
            return self.sub_ins()
        elif self.tok_matches(Tok.MUL_INS):
            return self.mul_ins()
        elif self.tok_matches(Tok.DIV_INS):
            return self.div_ins()
        elif self.tok_matches(Tok.PRINT_INS):
            return self.print_ins()

    def i32_ins(self):
        # i32_ins -> ^I32^ register i32_lit
        dest = self.register()
        lit = self.i32_lit()
        return I32Ins(dest, lit)

    def add_ins(self):
        # add_ins -> ^ADD^ register register register
        dest = self.register()
        src0 = self.register()
        src1 = self.register()
        return AddIns(dest, src0, src1)

    def sub_ins(self):
        # sub_ins -> ^SUB^ register register register
        dest = self.register()
        src0 = self.register()
        src1 = self.register()
        return SubIns(dest, src0, src1)

    def mul_ins(self):
        # mul_ins -> ^MUL^ register register register
        dest = self.register()
        src0 = self.register()
        src1 = self.register()
        return MulIns(dest, src0, src1)

    def div_ins(self):
        # div_ins -> ^DIV^ register register register
        dest = self.register()
        src0 = self.register()
        src1 = self.register()
        return DivIns(dest, src0, src1)

    def print_ins(self):
        # print_ins -> ^PRINT^ register
        return PrintIns(self.register())

    def register(self):
        if self.tok_matches(Tok.ID):
            lexeme = self.prev_tok.lexeme.lower()
            if lexeme.startswith("r"):
                try:
                    reg_index = int(lexeme[1:])
                    return Register(reg_index)
                except ValueError:
                    raise ParserError("[{}:{}] Not a valid register: {}"
                            .format(self.prev_tok.lineno,
                                    self.prev_tok.colno,
                                    lexeme))
            else:
                raise ParserError("[{}:{}] Expected a register"
                        .format(self.prev_tok.lineno, self.prev_tok.colno))

    def i32_lit(self):
        if self.tok_matches(Tok.I32_LIT):
            return I32Cons(self.prev_tok)
        else:
            raise ParserError(self.this_tok, "Expected a 32 bit integer")

    def tok_next(self):
        self.prev_tok = self.this_tok
        self.this_tok = self.lex.get_tok()
        return self.prev_tok

    def tok_matches(self, kind):
        if self.this_tok.kind == kind:
            self.tok_next()
            return True
        else:
            return False

    def tok_consume(self, kind, msg):
        if self.this_tok.kind == kind:
            self.tok_next()
        else:
            raise ParserError(self.this_tok, msg)

    def tok_is(self, kind_arr: List) -> bool:
        return self.this_tok.kind in kind_arr
