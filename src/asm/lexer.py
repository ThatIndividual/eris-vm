import string
from enum import Enum


class Tok(Enum):
    EOF = "TOK_EOF"

    ID = "TOK_ID"
    SUB = "TOK_SUB"
    DO = "TOK_DO"
    END = "TOK_END"
    ARGS = "TOK_ARGS"
    LOCS = "TOK_LOCS"
    LPAR = "TOK_LPAR"
    RPAR = "TOK_RPAR"
    EQ = "TOK_EQ"
    COMMA = "TOK_COMMA"

    DOUBLE = "TOK_DOUBLE"
    I32_LIT = "TOK_I32_LIT"
    FLT_LIT = "TOK_FLT_LIT"
    LABEL = "TOK_LABEL"
    AT_LOCATION = "TOK_AT_LOCATION"

    HALT_INS = "TOK_HALT_INS"
    NOOP_INS = "TOK_NOOP_INS"

    I32_INS = "TOK_I32_INS"
    FLT_INS = "TOK_FLT_INS"
    ADD_I32_INS = "TOK_I32_ADD_INS"
    SUB_I32_INS = "TOK_I32_SUB_INS"
    MUL_I32_INS = "TOK_I32_MUL_INS"
    DIV_I32_INS = "TOK_I32_DIV_INS"
    MOD_I32_INS = "TOK_I32_MOD_INS"

    ADD_FLT_INS = "TOK_FLT_ADD_INS"
    SUB_FLT_INS = "TOK_FLT_SUB_INS"
    MUL_FLT_INS = "TOK_FLT_MUL_INS"
    DIV_FLT_INS = "TOK_FLT_DIV_INS"

    I32_FLT_INS = "TOK_I32_FLT_INS"
    FLT_I32_INS = "TOK_FLT_I32_INS"

    CALL_INS = "TOK_CALL_INS"
    RECEIVE_INS = "TOK_RECEIVE_INS"
    RETURN_INS = "TOK_RETURN_INS"

    JMP_INS = "TOK_JMP_INS"
    JEQ_INS = "TOK_JEQ_INS"
    JNE_INS = "TOK_JNE_INS"
    JLT_INS = "TOK_JLT_INS"
    JLE_INS = "TOK_JLE_INS"
    JGT_INS = "TOK_JGT_INS"
    JGE_INS = "TOK_JGE_INS"
    JEQZ_INS = "TOK_JEQZ_INS"
    JNEZ_INS = "TOK_JNEZ_INS"
    JLTZ_INS = "TOK_JLTZ_INS"
    JLEZ_INS = "TOK_JLEZ_INS"
    JGTZ_INS = "TOK_JGTZ_INS"
    JGEZ_INS = "TOK_JGEZ_INS"

    MOVE_INS = "TOK_MOVE_INS"
    PRINT_INS = "TOK_PRINT_INS"


keywords = {
    "id": Tok.ID,
    "sub": Tok.SUB,
    "do": Tok.DO,
    "end": Tok.END,
    "args": Tok.ARGS,
    "locs": Tok.LOCS,

    "halt": Tok.HALT_INS,
    "noop": Tok.NOOP_INS,

    "i32": Tok.I32_INS,
    "flt": Tok.FLT_INS,
    "add.i32": Tok.ADD_I32_INS,
    "sub.i32": Tok.SUB_I32_INS,
    "mul.i32": Tok.MUL_I32_INS,
    "div.i32": Tok.DIV_I32_INS,
    "mod.i32": Tok.MOD_I32_INS,

    "add.flt": Tok.ADD_FLT_INS,
    "sub.flt": Tok.SUB_FLT_INS,
    "mul.flt": Tok.MUL_FLT_INS,
    "div.flt": Tok.DIV_FLT_INS,

    "i32.flt": Tok.I32_FLT_INS,
    "flt.i32": Tok.FLT_I32_INS,

    "call": Tok.CALL_INS,
    "receive": Tok.RECEIVE_INS,
    "return": Tok.RETURN_INS,

    "jmp": Tok.JMP_INS,
    "jeq": Tok.JEQ_INS,
    "jne": Tok.JNE_INS,
    "jlt": Tok.JLT_INS,
    "jle": Tok.JLE_INS,
    "jgt": Tok.JGT_INS,
    "jge": Tok.JGE_INS,
    "jeqz": Tok.JEQZ_INS,
    "jnez": Tok.JNEZ_INS,
    "jltz": Tok.JLTZ_INS,
    "jlez": Tok.JLEZ_INS,
    "jgtz": Tok.JGTZ_INS,
    "jgez": Tok.JGEZ_INS,

    "move": Tok.MOVE_INS,
    "print": Tok.PRINT_INS,
}


def is_alpha(c: str) -> bool:
    return c in string.ascii_letters


def is_num(c: str) -> bool:
    return c in string.digits


def is_alpha_num(c: str) -> bool:
    return is_alpha(c) or is_num(c) or c == "."


class LexerError(Exception):
    def __init__(self, msg, lineno):
        self.msg = msg
        self.lineno = lineno


class Token:
    def __init__(self, lexeme, kind, lineno, colno):
        self.lexeme = lexeme
        self.kind = kind
        self.lineno = lineno
        self.colno = colno

    def __repr__(self):
        return "({} @ {},{})".format(self.lexeme, self.lineno, self.colno)


class Lexer:
    def __init__(self):
        self.buffer = None
        self.index = 0
        self.start = 0
        self.lineno = 1
        self.colno = 0

    def feed(self, buf):
        self.index = 0
        self.buffer = buf

    def char_next(self) -> str:
        char = self.buffer[self.index]
        self.index += 1
        self.colno += 1
        return char

    def lookahead(self) -> str:
        return self.buffer[self.index]

    def is_at_end(self) -> bool:
        return self.buffer[self.index] == '\0'

    def char_matches(self, char: str) -> bool:
        if self.is_at_end():
            return False
        elif self.buffer[self.index] == char:
            self.char_next()
            return True
        else:
            return False

    def tok(self, kind) -> Token:
        lexeme = self.buffer[self.start:self.index]
        length = self.index - self.start
        return Token(lexeme, kind, self.lineno, self.colno - length)

    def get_tok(self) -> Token:
        self.skip_space()
        self.start = self.index
        char = self.char_next()

        if is_alpha(char):
            return self.identifier()
        elif is_num(char) or char == '-':
            return self.number()
        elif char == "\0":
            return self.tok(Tok.EOF)
        elif char == "@":
            return self.at_location()
        elif char == "(":
            return self.tok(Tok.LPAR)
        elif char == ")":
            return self.tok(Tok.RPAR)
        elif char == "=":
            return self.tok(Tok.EQ)
        elif char == ",":
            return self.tok(Tok.COMMA)

        raise LexerError("Unknown character: '{}'".format(char), self.lineno)

    def identifier(self) -> Token:
        while is_alpha_num(self.lookahead()):
            self.char_next()
        if self.char_matches(':'):
            return self.tok(Tok.LABEL)
        else:
            tok = self.tok(Tok.ID)
            lexeme = tok.lexeme.lower()
            if lexeme in keywords:
                tok.kind = keywords[lexeme]

            return tok

    def number(self) -> Token:
        is_double = False

        while True:
            if is_num(self.lookahead()):
                self.char_next()
            elif self.char_matches("."):
                if not is_double:
                    is_double = True
                    self.char_next()
                else:
                    break
            else:
                break

        if is_double:
            return self.tok(Tok.FLT_LIT)
        else:
            return self.tok(Tok.I32_LIT)

    def at_location(self):
        self.start = self.index
        while is_alpha_num(self.lookahead()):
            self.char_next()
        return self.tok(Tok.AT_LOCATION)

    def skip_space(self):
        while True:
            char = self.lookahead()
            if char in " \r\t":
                self.char_next()
            elif char == "\n":
                self.lineno += 1
                self.colno = 0
                self.char_next()
            else:
                break

    def skip_line(self):
        while True:
            char = self.lookahead()
            if char == "\n":
                self.lineno += 1
                self.colno = 0
                self.char_next()
                break
            elif char == '\0':
                break
            else:
                self.char_next()
