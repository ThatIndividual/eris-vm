from typing import List

from ast import *
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
        # program -> sub* "EOF"
        sections = []
        while not self.tok_is([Tok.EOF]):
            sections.append(self.sub())
        return Program(sections)

    def sub(self):
        # sub -> "sub" identifier "(" "args" "=" int "," "locs" "=" int ")" "do"
        #                (name? instruction)*
        #        "end"
        args = 0
        locs = 0

        self.tok_consume(Tok.SUB, "Expected the beginning of a sub")
        self.tok_consume(Tok.ID, "A sub name should follow the `sub` keyword")
        id = self.prev_tok
        self.tok_consume(Tok.LPAR, "Expected an opening paren after subroutine name")
        self.tok_consume(Tok.ARGS, "Expected an \"args\" argument.")
        self.tok_consume(Tok.EQ, "Expected an equals after \"args\" argument")
        args = self.lit_i32()
        self.tok_consume(Tok.COMMA, "Expected a comma separating \"args\" from \"locs\"")
        self.tok_consume(Tok.LOCS, "Expected a \"locs\" argument.")
        self.tok_consume(Tok.EQ, "Expected an equals after \"locs\" argument")
        locs = self.lit_i32()
        self.tok_consume(Tok.RPAR, "Expected a closing paren after subroutine "
                                   "argument list")
        self.tok_consume(Tok.DO, "Expected a `do ... end` block after sub definition")

        ins = []
        while not self.tok_is([Tok.END, Tok.EOF]):
            if self.tok_is([Tok.LABEL]):
                ins.append(self.label())
            ins.append(self.ins())
        self.tok_consume(Tok.END, "Missing `end` keyword after block")
        return SubStm(id, ins, args, locs)

    def ins(self):
        # instructions
        #   -> halt_ins | noop_ins |
        #    | i32_ins
        #    | add_ins | sub_ins | mul_ins | div_ins | mod_ins
        #    | call_ins | ret_ins
        #    | jmp_ins
        #    | jeq_ins | jne_ins | jlt_ins | jle_ins | jgt_ins | jge_ins
        #    | jeqz_ins | jnez_ins | jltz_ins | jlez_ins | jgtz_ins | jgez_ins
        #    | move_ins
        #    | print_ins
        if self.tok_matches(Tok.HALT_INS):
            return HaltIns()
        elif self.tok_matches(Tok.NOOP_INS):
            return NoopIns()
        elif self.tok_matches(Tok.I32_INS):
            return self.i32_ins()

        elif self.tok_matches(Tok.ADD_INS):
            return self.add_ins()
        elif self.tok_matches(Tok.SUB):
            return self.sub_ins()
        elif self.tok_matches(Tok.MUL_INS):
            return self.mul_ins()
        elif self.tok_matches(Tok.DIV_INS):
            return self.div_ins()
        elif self.tok_matches(Tok.MOD_INS):
            return self.mod_ins()

        elif self.tok_matches(Tok.CALL_INS):
            return self.call_ins()
        elif self.tok_matches(Tok.RET_INS):
            return self.ret_ins()

        elif self.tok_matches(Tok.JMP_INS):
            return self.jmp_ins()
        elif self.tok_matches(Tok.JEQ_INS):
            return self.jeq_ins()
        elif self.tok_matches(Tok.JNE_INS):
            return self.jne_ins()
        elif self.tok_matches(Tok.JLT_INS):
            return self.jlt_ins()
        elif self.tok_matches(Tok.JLE_INS):
            return self.jle_ins()
        elif self.tok_matches(Tok.JGT_INS):
            return self.jgt_ins()
        elif self.tok_matches(Tok.JGE_INS):
            return self.jge_ins()
        elif self.tok_matches(Tok.JEQZ_INS):
            return self.jeqz_ins()
        elif self.tok_matches(Tok.JNEZ_INS):
            return self.jnez_ins()
        elif self.tok_matches(Tok.JLTZ_INS):
            return self.jltz_ins()
        elif self.tok_matches(Tok.JLEZ_INS):
            return self.jlez_ins()
        elif self.tok_matches(Tok.JGTZ_INS):
            return self.jgtz_ins()
        elif self.tok_matches(Tok.JGEZ_INS):
            return self.jgez_ins()

        elif self.tok_matches(Tok.MOVE_INS):
            return self.move_ins()
        elif self.tok_matches(Tok.PRINT_INS):
            return self.print_ins()
        else:
            raise ParserError("Expected an instruction, got {}".format(self.this_tok.lexeme))

    def i32_ins(self):
        # i32_ins -> ^I32^ lit_i32 register
        lit = self.lit_i32()
        dest = self.register()
        return CnsI32Ins(lit, dest)

    def add_ins(self):
        # add_ins -> ^ADD^ register register register
        src0 = self.register()
        src1 = self.register()
        dest = self.register()
        return AddIns(src0, src1, dest)

    def sub_ins(self):
        # sub_ins -> ^SUB^ register register register
        src0 = self.register()
        src1 = self.register()
        dest = self.register()
        return SubIns(src0, src1, dest)

    def mul_ins(self):
        # mul_ins -> ^MUL^ register register register
        src0 = self.register()
        src1 = self.register()
        dest = self.register()
        return MulIns(src0, src1, dest)

    def div_ins(self):
        # div_ins -> ^DIV^ register register register
        src0 = self.register()
        src1 = self.register()
        dest = self.register()
        return DivIns(src0, src1, dest)

    def mod_ins(self):
        # mod_ins -> ^MOD^ register register register
        src0 = self.register()
        src1 = self.register()
        dest = self.register()
        return ModIns(src0, src1, dest)

    def call_ins(self):
        # call_ins -> ^CALL^ id register register
        self.tok_consume(Tok.ID, "Expected a subroutine name")
        id = self.prev_tok
        src0 = self.register()
        dest = self.register()
        return CallIns(id, src0, dest)

    def ret_ins(self):
        # ret_ins -> ^RET^ register
        src0 = self.register()
        return RetIns(src0)

    def jmp_ins(self):
        # jmp_ins -> ^JMP^ at_location
        return JmpIns(self.at_location())

    def jeq_ins(self):
        # jeq_ins -> ^JEQ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JeqIns(at_location, src0, src1)

    def jne_ins(self):
        # jne_ins -> ^JNE^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JneIns(at_location, src0, src1)

    def jlt_ins(self):
        # jlt_ins -> ^JLT^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JltIns(at_location, src0, src1)

    def jle_ins(self):
        # jle_ins -> ^JLE^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JleIns(at_location, src0, src1)

    def jgt_ins(self):
        # jgt_ins -> ^JGT^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JgtIns(at_location, src0, src1)

    def jge_ins(self):
        # jge_ins -> ^JGE^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JgeIns(at_location, src0, src1)

    def jeqz_ins(self):
        # jeqz_ins -> ^JEQZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JeqzIns(at_location, src0, src1)

    def jnez_ins(self):
        # jnez_ins -> ^JNEZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JnezIns(at_location, src0, src1)

    def jltz_ins(self):
        # jltz_ins -> ^JLTZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JltzIns(at_location, src0, src1)

    def jlez_ins(self):
        # jlez_ins -> ^JLEZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JlezIns(at_location, src0, src1)

    def jgtz_ins(self):
        # jgtz_ins -> ^JGTZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JgtzIns(at_location, src0, src1)

    def jgez_ins(self):
        # jgez_ins -> ^JGEZ^ at_location register register
        at_location = self.at_location()
        src0 = self.register()
        src1 = self.register()
        return JgezIns(at_location, src0, src1)

    def move_ins(self):
        # move_ins -> ^MOVE^ register register
        src0 = self.register()
        dest = self.register()
        return MoveIns(src0, dest)

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

    def lit_i32(self):
        if self.tok_matches(Tok.I32_LIT):
            return LitI32(self.prev_tok)
        else:
            raise ParserError(self.this_tok, "Expected a 32 bit integer")

    def label(self):
        if self.tok_matches(Tok.LABEL):
            return Label(self.prev_tok.lexeme.lower())
        else:
            raise ParserError("Expected a label")

    def at_location(self):
        if self.tok_matches(Tok.AT_LOCATION):
            return AtLocation(self.prev_tok.lexeme.lower())
        else:
            raise ParserError("Expected an at-location")

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
