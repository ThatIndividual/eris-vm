import string
from enum import Enum


class Tok(Enum):
    EOF = "TOK_EOF"

    ID = "TOK_ID"
    SECTION = "TOK_SECTION"
    DO = "TOK_DO"
    END = "TOK_END"

    DOUBLE = "TOK_DOUBLE"
    I32_LIT = "TOK_I32_LIT"

    I32_INS = "TOK_I32_INS"
    ADD_INS = "TOK_ADD_INS"
    SUB_INS = "TOK_SUB_INS"
    MUL_INS = "TOK_MUL_INS"
    DIV_INS = "TOK_DIV_INS"

    PRINT_INS = "TOK_PRINT"


keywords = {
    "id": Tok.ID,
    "section": Tok.SECTION,
    "do": Tok.DO,
    "end": Tok.END,

    "i32": Tok.I32_INS,
    "add": Tok.ADD_INS,
    "sub": Tok.SUB_INS,
    "mul": Tok.MUL_INS,
    "div": Tok.DIV_INS,

    "print": Tok.PRINT_INS,

}


def is_alpha(c: str) -> bool:
    return c in string.ascii_letters


def is_num(c: str) -> bool:
    return c in string.digits


def is_alpha_num(c: str) -> bool:
    return is_alpha(c) or is_num(c)


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
        if is_num(char):
            return self.number()

        if char == "\0":
            return self.tok(Tok.EOF)
        else:
            raise LexerError("Unknown character: '{}'".format(char), self.lineno)

    def identifier(self) -> Token:
        while is_alpha_num(self.lookahead()):
            self.char_next()

        tok = self.tok(Tok.ID)
        if tok.lexeme in keywords:
            tok.kind = keywords[tok.lexeme.lower()]

        return tok

    def number(self) -> Token:
        is_double = False

        while True:
            if is_num(self.lookahead()):
                self.char_next()
            elif self.lookahead() == ".":
                if not is_double:
                    is_double = True
                    self.char_next()
                else:
                    break
            else:
                break

        if is_double:
            raise LexerError("Floats are not supported")
        else:
            return self.tok(Tok.I32_LIT)

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
