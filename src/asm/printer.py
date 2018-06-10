from visitor import AbstractVisitor
from ast import *


class PrintVisitor(AbstractVisitor):
    @classmethod
    def print(cls, node):
        return node.accept(cls)

    @classmethod
    def visit_program(cls, program: Program):
        return "\n".join([cls.print(section) for section in program.subs])

    @classmethod
    def visit_sub_stm(cls, sub_stm: SubStm):
        return "sub {}(args={}, locs={}) do\n{}\nend\n".format(
            sub_stm.id.lexeme,
            cls.print(sub_stm.args),
            cls.print(sub_stm.locs),
            "\n".join([cls.print(i) for i in sub_stm.instructions])
        )

    @classmethod
    def visit_halt_ins(cls, halt_ins: HaltIns):
        return "    HALT"

    @classmethod
    def visit_noop_ins(cls, noop_ins: NoopIns):
        return "    NOOP"

    @classmethod
    def visit_cns_i32_ins(cls, cns_i32_ins: CnsI32Ins):
        return "    I32 {} {}".format(cls.print(cns_i32_ins.lit_i32),
                                      cls.print(cns_i32_ins.dest))

    @classmethod
    def visit_add_ins(cls, add_stm: AddIns):
        return "    ADD {} {} {}".format(cls.print(add_stm.src0),
                                         cls.print(add_stm.src1),
                                         cls.print(add_stm.dest))

    @classmethod
    def visit_sub_ins(cls, sub_stm: SubIns):
        return "    SBT {} {} {}".format(cls.print(sub_stm.src0),
                                         cls.print(sub_stm.src1),
                                         cls.print(sub_stm.dest))

    @classmethod
    def visit_mul_ins(cls, mul_stm: MulIns):
        return "    MUL {} {} {}".format(cls.print(mul_stm.src0),
                                         cls.print(mul_stm.src1),
                                         cls.print(mul_stm.dest))

    @classmethod
    def visit_div_ins(cls, div_stm: DivIns):
        return "    DIV {} {} {}".format(cls.print(div_stm.src0),
                                         cls.print(div_stm.src1),
                                         cls.print(div_stm.dest))

    @classmethod
    def visit_mod_ins(cls, mod_ins: ModIns):
        return "    MOD {} {} {}".format(cls.print(mod_ins.src0),
                                         cls.print(mod_ins.src1),
                                         cls.print(mod_ins.dest))

    @classmethod
    def visit_call_ins(cls, call_ins: CallIns):
        call = "    CALL {}[{}] {}".format(call_ins.id.lexeme, call_ins.sub, len(call_ins.src))
        for vreg in call_ins.src:
            call += " {}".format(cls.print(vreg))
        return call

    @classmethod
    def visit_receive_ins(cls, receive_ins: ReceiveIns):
        return "    RECEIVE {}".format(cls.print(receive_ins.src))

    @classmethod
    def visit_ret_ins(cls, ret_ins: RetIns):
        if ret_ins.src0:
            return "    RETURN {}".format(cls.print(ret_ins.src0))
        else:
            return "    RETURN"

    @classmethod
    def visit_jmp_ins(cls, jmp_ins: JmpIns):
        return "    JMP {}".format(cls.print(jmp_ins.at_location))

    @classmethod
    def visit_jeq_ins(cls, jeq_ins: JeqIns):
        return "    JEQ {} {} {}".format(cls.print(jeq_ins.at_location),
                                         cls.print(jeq_ins.src0),
                                         cls.print(jeq_ins.src1))

    @classmethod
    def visit_jne_ins(cls, jne_ins: JneIns):
        return "    JNE {} {} {}".format(cls.print(jne_ins.at_location),
                                         cls.print(jne_ins.src0),
                                         cls.print(jne_ins.src1))

    @classmethod
    def visit_jlt_ins(cls, jlt_ins: JltIns):
        return "    JLT {} {} {}".format(cls.print(jlt_ins.at_location),
                                         cls.print(jlt_ins.src0),
                                         cls.print(jlt_ins.src1))

    @classmethod
    def visit_jle_ins(cls, jle_ins: JleIns):
        return "    JLE {} {} {}".format(cls.print(jle_ins.at_location),
                                         cls.print(jle_ins.src0),
                                         cls.print(jle_ins.src1))

    @classmethod
    def visit_jgt_ins(cls, jgt_ins: JgtIns):
        return "    JGT {} {} {}".format(cls.print(jgt_ins.at_location),
                                         cls.print(jgt_ins.src0),
                                         cls.print(jgt_ins.src1))

    @classmethod
    def visit_jge_ins(cls, jge_ins: JgeIns):
        return "    JGE {} {} {}".format(cls.print(jge_ins.at_location),
                                         cls.print(jge_ins.src0),
                                         cls.print(jge_ins.src1))

    @classmethod
    def visit_jeqz_ins(cls, jeqz_ins: JeqzIns):
        return "    JGEZ {} {}".format(cls.print(jeqz_ins.at_location),
                                          cls.print(jeqz_ins.src0))

    @classmethod
    def visit_jnez_ins(cls, jnez_ins: JnezIns):
        return "    JNEZ {} {}".format(cls.print(jnez_ins.at_location),
                                          cls.print(jnez_ins.src0))

    @classmethod
    def visit_jltz_ins(cls, jltz_ins: JltzIns):
        return "    JLTZ {} {}".format(cls.print(jltz_ins.at_location),
                                          cls.print(jltz_ins.src0))

    @classmethod
    def visit_jlez_ins(cls, jlez_ins: JlezIns):
        return "    JLEZ {} {}".format(cls.print(jlez_ins.at_location),
                                          cls.print(jlez_ins.src0))

    @classmethod
    def visit_jgtz_ins(cls, jgtz_ins: JgtzIns):
        return "    JGTZ {} {}".format(cls.print(jgtz_ins.at_location),
                                          cls.print(jgtz_ins.src0))

    @classmethod
    def visit_jgez_ins(cls, jgez_ins: JgezIns):
        return "    JGEZ {} {}".format(cls.print(jgez_ins.at_location),
                                          cls.print(jgez_ins.src0))

    @classmethod
    def visit_move_ins(cls, move_ins: MoveIns):
        return "    MOVE {} {}".format(cls.print(move_ins.src0),
                                       cls.print(move_ins.dest))

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
