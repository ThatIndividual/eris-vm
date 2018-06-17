from struct import pack

from ast import *
from visitor import AbstractVisitor

bytecode = {
    "halt": b"\x00",
    "noop": b"\x01",
    "add_i32": b"\x02",
    "sub_i32": b"\x03",
    "mul_i32": b"\x04",
    "div_i32": b"\x05",
    "mod_i32": b"\x06",
    "add_flt": b"\x07",
    "sub_flt": b"\x08",
    "mul_flt": b"\x09",
    "div_flt": b"\x0A",
    "i32_flt": b"\x0B",
    "flt_i32": b"\x0C",
    "call": b"\x0D",
    "receive": b"\x0E",
    "return": b"\x0F",
    "return_nil": b"\x10",
    "jmp": b"\x11",
    "jmp_eq": b"\x12",
    "jmp_ne": b"\x13",
    "jmp_lt": b"\x14",
    "jmp_le": b"\x15",
    "jmp_gt": b"\x16",
    "jmp_ge": b"\x17",
    "jmp_eqz": b"\x18",
    "jmp_nez": b"\x19",
    "jmp_ltz": b"\x1A",
    "jmp_lez": b"\x1B",
    "jmp_gtz": b"\x1C",
    "jmp_gez": b"\x1D",
    "cns_chr": b"\x1E",
    "cns_i32": b"\x1F",
    "cns_flt": b"\x20",
    "cns_str": b"\x21",
    "load_glb": b"\x22",
    "store_glb": b"\x23",
    "move": b"\x24",
    "print": b"\x25",
}


class AssemblerError(Exception):
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg


class AssemblerVisitor(AbstractVisitor):
    def __init__(self):
        self.sub_descriptions = []
        self.current_sub = None

    def assemble(self, node):
        return node.accept(self)

    def visit_program(self, program: Program):
        header = b"\xCA\x11\x15\x71"
        maj_ver = pack("<H", 0)
        min_ver = pack("<H", 4)

        entry_code = self.assemble(program.subs[0])
        other_code = b"".join([self.assemble(sub) for sub in program.subs[1:]])
        ins_code = entry_code + other_code

        sub_desc = b""
        for sd in self.sub_descriptions:
            sub_desc += pack("<I", sd[0]) + \
                        pack("<H", sd[1]) + \
                        pack("<H", sd[2])

        sub_desc_size = pack("<I", len(self.sub_descriptions))
        ins_size = pack("<I", len(ins_code))

        return header + maj_ver + min_ver + \
               sub_desc_size + ins_size + \
               sub_desc + ins_code

    def visit_sub_stm(self, sub_stm: SubStm):
        self.current_sub = sub_stm
        self.sub_descriptions.append((sub_stm.address,
                                      int(sub_stm.args.i32_tok.lexeme),
                                      int(sub_stm.locs.i32_tok.lexeme)))
        return b"".join([self.assemble(statement) for statement in sub_stm.instructions])

    def visit_halt_ins(self, hlt_ins: HaltIns):
        return bytecode["halt"]

    def visit_noop_ins(self, nop_ins: NoopIns):
        return bytecode["noop"]

    def visit_cns_i32_ins(self, cns_i32_ins: CnsI32Ins):
        return bytecode["cns_i32"] + self.assemble(cns_i32_ins.lit_i32) + \
               self.assemble(cns_i32_ins.dest)

    def visit_cns_flt_ins(self, cns_flt_ins: CnsFltIns):
        return bytecode["cns_flt"] + self.assemble(cns_flt_ins.lit_flt) + \
               self.assemble(cns_flt_ins.dest)

    def visit_add_i32_ins(self, add_ins: AddI32Ins):
        return bytecode["add_i32"] + \
               self.assemble(add_ins.src0) + \
               self.assemble(add_ins.src1) + \
               self.assemble(add_ins.dest)

    def visit_sub_i32_ins(self, sub_ins: SubI32Ins):
        return bytecode["sub_i32"] + \
               self.assemble(sub_ins.src0) + \
               self.assemble(sub_ins.src1) + \
               self.assemble(sub_ins.dest)

    def visit_mul_i32_ins(self, mul_ins: MulI32Ins):
        return bytecode["mul_i32"] + \
               self.assemble(mul_ins.src0) + \
               self.assemble(mul_ins.src1) + \
               self.assemble(mul_ins.dest)

    def visit_div_i32_ins(self, div_ins: DivI32Ins):
        return bytecode["div_i32"] + \
               self.assemble(div_ins.src0) + \
               self.assemble(div_ins.src1) + \
               self.assemble(div_ins.dest)

    def visit_mod_i32_ins(self, mod_ins: ModI32Ins):
        return bytecode["mod_i32"] + \
               self.assemble(mod_ins.src0) + \
               self.assemble(mod_ins.src1) + \
               self.assemble(mod_ins.dest)

    def visit_add_flt_ins(self, add_ins: AddFltIns):
        return bytecode["add_flt"] + \
               self.assemble(add_ins.src0) + \
               self.assemble(add_ins.src1) + \
               self.assemble(add_ins.dest)

    def visit_sub_flt_ins(self, sub_ins: SubFltIns):
        return bytecode["sub_flt"] + \
               self.assemble(sub_ins.src0) + \
               self.assemble(sub_ins.src1) + \
               self.assemble(sub_ins.dest)

    def visit_mul_flt_ins(self, mul_ins: MulFltIns):
        return bytecode["mul_flt"] + \
               self.assemble(mul_ins.src0) + \
               self.assemble(mul_ins.src1) + \
               self.assemble(mul_ins.dest)

    def visit_div_flt_ins(self, div_ins: DivFltIns):
        return bytecode["div_flt"] + \
               self.assemble(div_ins.src0) + \
               self.assemble(div_ins.src1) + \
               self.assemble(div_ins.dest)

    def visit_i32_flt_ins(self, i32_flt: I32FltIns):
        return bytecode["i32_flt"] + \
               self.assemble(i32_flt.src0) + \
               self.assemble(i32_flt.dest)

    def visit_flt_i32_ins(self, flt_i32: FltI32Ins):
        return bytecode["flt_i32"] + \
               self.assemble(flt_i32.src0) + \
               self.assemble(flt_i32.dest)

    def visit_call_ins(self, call_ins: CallIns):
        code = bytecode["call"] + pack("<B", call_ins.sub) + pack("<B", len(call_ins.src))
        for vreg in call_ins.src:
            code += self.assemble(vreg)
        return code

    def visit_receive_ins(self, receive_ins: ReceiveIns):
        return bytecode["receive"] + \
               self.assemble(receive_ins.src)

    def visit_ret_ins(self, ret_ins: RetIns):
        if ret_ins.src0:
            return bytecode["return"] + \
                   self.assemble(ret_ins.src0)
        else:
            return bytecode["return_nil"]

    def visit_jmp_ins(self, jmp_ins: JmpIns):
        return bytecode["jmp"] + self.assemble(jmp_ins.at_location)

    def visit_jeq_ins(self, jeq_ins: JeqIns):
        return bytecode["jmp_eq"] + \
               self.assemble(jeq_ins.at_location) + \
               self.assemble(jeq_ins.src0) + \
               self.assemble(jeq_ins.src1)

    def visit_jne_ins(self, jne_ins: JneIns):
        return bytecode["jmp_ne"] + \
               self.assemble(jne_ins.at_location) + \
               self.assemble(jne_ins.src0) + \
               self.assemble(jne_ins.src1)

    def visit_jlt_ins(self, jlt_ins: JltIns):
        return bytecode["jmp_lt"] + \
               self.assemble(jlt_ins.at_location) + \
               self.assemble(jlt_ins.src0) + \
               self.assemble(jlt_ins.src1)

    def visit_jle_ins(self, jle_ins: JleIns):
        return bytecode["jmp_le"] + \
               self.assemble(jle_ins.at_location) + \
               self.assemble(jle_ins.src0) + \
               self.assemble(jle_ins.src1)

    def visit_jgt_ins(self, jgt_ins: JgtIns):
        return bytecode["jmp_gt"] + \
               self.assemble(jgt_ins.at_location) + \
               self.assemble(jgt_ins.src0) + \
               self.assemble(jgt_ins.src1)

    def visit_jge_ins(self, jge_ins: JgeIns):
        return bytecode["jmp_ge"] + \
               self.assemble(jge_ins.at_location) + \
               self.assemble(jge_ins.src0) + \
               self.assemble(jge_ins.src1)

    def visit_jeqz_ins(self, jeqz_ins: JeqzIns):
        return bytecode["jmp_eqz"] + \
               self.assemble(jeqz_ins.at_location) + \
               self.assemble(jeqz_ins.src0)

    def visit_jnez_ins(self, jnez_ins: JnezIns):
        return bytecode["jmp_nez"] + \
               self.assemble(jnez_ins.at_location) + \
               self.assemble(jnez_ins.src0)

    def visit_jltz_ins(self, jltz_ins: JltzIns):
        return bytecode["jmp_ltz"] + \
               self.assemble(jltz_ins.at_location) + \
               self.assemble(jltz_ins.src0)

    def visit_jlez_ins(self, jlez_ins: JlezIns):
        return bytecode["jmp_lez"] + \
               self.assemble(jlez_ins.at_location) + \
               self.assemble(jlez_ins.src0)

    def visit_jgtz_ins(self, jgtz_ins: JgtzIns):
        return bytecode["jmp_gtz"] + \
               self.assemble(jgtz_ins.at_location) + \
               self.assemble(jgtz_ins.src0)

    def visit_jgez_ins(self, jgez_ins: JgezIns):
        return bytecode["jmp_gez"] + \
               self.assemble(jgez_ins.at_location) + \
               self.assemble(jgez_ins.src0)

    def visit_move_ins(self, move_ins: MoveIns):
        return bytecode["move"] + \
               self.assemble(move_ins.src0) + \
               self.assemble(move_ins.dest)

    def visit_print_ins(self, print_ins: PrintIns):
        return bytecode["print"] + \
               self.assemble(print_ins.src0)

    def visit_register(self, reg: Register):
        n = reg.reg_num
        regs = int(self.current_sub.args.i32_tok.lexeme) + \
               int(self.current_sub.locs.i32_tok.lexeme) - 1
        return pack("<B", regs - n)

    def visit_lit_i32(self, lit_i32: LitI32):
        return pack("<i", int(lit_i32.i32_tok.lexeme))

    def visit_lit_flt(self, lit_flt: LitFlt):
        return pack("<f", float(lit_flt.flt_tok.lexeme))

    def visit_label(self, label: Label):
        return b""

    def visit_at_location(self, at_location: AtLocation):
        return pack("<b", at_location.address)
