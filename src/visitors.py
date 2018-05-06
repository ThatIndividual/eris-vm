from ast import Section, AddIns, SubIns, MulIns, DivIns, PrintIns, I32Cons, ProgramAst, Register
from lexer import Token


class PrintVisitor:
    @classmethod
    def print(cls, node):
        return node.accept(cls)

    @classmethod
    def visit_program(cls, program: ProgramAst):
        return "".join([cls.print(section) for section in program.sections])

    @classmethod
    def visit_section(cls, section_stm: Section):
        return "section {} do\n{}end\n\n".format(
            section_stm.id.lexeme,
            "".join(["    {}\n".format(cls.print(i)) for i in section_stm.instructions])
        )

    @classmethod
    def visit_i32_ins(cls, i32_stm: I32Cons):
        return "I32 {} {}".format(cls.print(i32_stm.dest), cls.print(i32_stm.src0))

    @classmethod
    def visit_add_ins(cls, add_stm: AddIns):
        return "ADD {} {} {}".format(cls.print(add_stm.dest),
                                     cls.print(add_stm.src0),
                                     cls.print(add_stm.src1))

    @classmethod
    def visit_sub_ins(cls, sub_stm: SubIns):
        return "SUB {} {} {}".format(cls.print(sub_stm.dest),
                                     cls.print(sub_stm.src0),
                                     cls.print(sub_stm.src1))

    @classmethod
    def visit_mul_ins(cls, mul_stm: MulIns):
        return "MUL {} {} {}".format(cls.print(mul_stm.dest),
                                     cls.print(mul_stm.src0),
                                     cls.print(mul_stm.src1))

    @classmethod
    def visit_div_ins(cls, div_stm: DivIns):
        return "DIV {} {} {}".format(cls.print(div_stm.dest),
                                     cls.print(div_stm.src0),
                                     cls.print(div_stm.src1))

    @classmethod
    def visit_print_ins(cls, print_stm: PrintIns):
        return "PRINT {}".format(cls.print(print_stm.src0))

    @classmethod
    def visit_i32_cons(cls, i32_lit: I32Cons):
        return i32_lit.i32_tok.lexeme

    @classmethod
    def visit_register(cls, reg: Register):
        return "R{}".format(reg.reg_num)


class AssemblyError(Exception):
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg


class AssemblyVisitor:
    @classmethod
    def assemble(cls, node):
        return node.accept(cls)

    @classmethod
    def visit_program(cls, program: ProgramAst):
        header = b"KNOT"
        maj_ver = (0).to_bytes(2, 'little')
        min_ver = (3).to_bytes(2, 'little')

        byte_code = b"".join([cls.assemble(section)
                              for section in program.sections])

        cns_size = (0).to_bytes(4, 'little')
        ins_size = len(byte_code).to_bytes(4, 'little')

        return header + maj_ver + min_ver + cns_size + ins_size + byte_code

    @classmethod
    def visit_section(cls, section: Section):
        return b"".join([cls.assemble(instruction)
                         for instruction in section.instructions])

    @classmethod
    def visit_i32_ins(cls, i32_ins: I32Cons):
        return b"\x16" + cls.assemble(i32_ins.dest) + \
               cls.assemble(i32_ins.src0)

    @classmethod
    def visit_add_ins(cls, add_ins: AddIns):
        return b"\x02" + cls.assemble(add_ins.dest) + \
               cls.assemble(add_ins.src0) + \
               cls.assemble(add_ins.src1)

    @classmethod
    def visit_sub_ins(cls, sub_ins: AddIns):
        return b"\x03" + cls.assemble(sub_ins.dest) + \
               cls.assemble(sub_ins.src0) + \
               cls.assemble(sub_ins.src1)

    @classmethod
    def visit_mul_ins(cls, mul_ins: AddIns):
        return b"\x04" + cls.assemble(mul_ins.dest) + \
               cls.assemble(mul_ins.src0) + \
               cls.assemble(mul_ins.src1)

    @classmethod
    def visit_div_ins(cls, div_ins: AddIns):
        return b"\x05" + cls.assemble(div_ins.dest) + \
               cls.assemble(div_ins.src0) + \
               cls.assemble(div_ins.src1)

    @classmethod
    def visit_print_ins(cls, print_ins: PrintIns):
        return b"\x1C" + cls.assemble(print_ins.src0)

    @classmethod
    def visit_i32_cons(cls, i32_cons: I32Cons):
        return int(i32_cons.i32_tok.lexeme).to_bytes(4, "little")

    @classmethod
    def visit_register(cls, reg: Register):
        return reg.reg_num.to_bytes(1, "little")
