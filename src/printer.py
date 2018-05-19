from visitor import AbstractVisitor
from ast import *


class PrintVisitor(AbstractVisitor):
    @classmethod
    def print(cls, node):
        return node.accept(cls)

    @classmethod
    def visit_program(cls, program: Program):
        return "".join([cls.print(section) for section in program.sections])

    @classmethod
    def visit_section(cls, section_stm: Section):
        return "section {} do\n{}end\n".format(
            section_stm.id.lexeme,
            "".join(["{}\n".format(cls.print(i)) for i in section_stm.instructions])
        )

    @classmethod
    def visit_cns_i32_ins(cls, cns_i32_ins: CnsI32Ins):
        return "    I32 {} {}".format(cls.print(cns_i32_ins.dest),
                                      cls.print(cns_i32_ins.lit_i32))

    @classmethod
    def visit_add_ins(cls, add_stm: AddIns):
        return "    ADD {} {} {}".format(cls.print(add_stm.dest),
                                         cls.print(add_stm.src0),
                                         cls.print(add_stm.src1))

    @classmethod
    def visit_sub_ins(cls, sub_stm: SubIns):
        return "    SUB {} {} {}".format(cls.print(sub_stm.dest),
                                         cls.print(sub_stm.src0),
                                         cls.print(sub_stm.src1))

    @classmethod
    def visit_mul_ins(cls, mul_stm: MulIns):
        return "    MUL {} {} {}".format(cls.print(mul_stm.dest),
                                         cls.print(mul_stm.src0),
                                         cls.print(mul_stm.src1))

    @classmethod
    def visit_div_ins(cls, div_stm: DivIns):
        return "    DIV {} {} {}".format(cls.print(div_stm.dest),
                                         cls.print(div_stm.src0),
                                         cls.print(div_stm.src1))

    @classmethod
    def visit_jump_ins(cls, jump_ins: JumpIns):
        return "    JUMP {}".format(cls.print(jump_ins.at_location))

    @classmethod
    def visit_jeq_ins(cls, jeq_ins: JeqIns):
        return "    JEQ {} {} {}".format(cls.print(jeq_ins.at_location),
                                         cls.print(jeq_ins.src0),
                                         cls.print(jeq_ins.src1))

    @classmethod
    def visit_jlt_ins(cls, jlt_ins: JltIns):
        return "    JLT {} {} {}".format(cls.print(jlt_ins.at_location),
                                         cls.print(jlt_ins.src0),
                                         cls.print(jlt_ins.src1))

    @classmethod
    def visit_move_ins(cls, move_ins: MoveIns):
        return "    MOVE {} {}".format(cls.print(move_ins.dest),
                                       cls.print(move_ins.src0))

    @classmethod
    def visit_print_ins(cls, print_stm: PrintIns):
        return "    PRINT {}".format(cls.print(print_stm.src0))

    @classmethod
    def visit_lit_i32(cls, lit_i32: LitI32):
        return lit_i32.i32_tok.lexeme

    @classmethod
    def visit_register(cls, reg: Register):
        return "R{}".format(reg.reg_num)

    @classmethod
    def visit_label(cls, label: Label):
        return "{}:".format(label.name)

    @classmethod
    def visit_at_location(cls, at_location: AtLocation):
        result = "@{}".format(at_location.name)
        if at_location.address is not None:
            result += "[{}]".format(at_location.address)
        return result
