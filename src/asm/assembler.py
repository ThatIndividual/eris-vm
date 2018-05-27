import struct

from ast import *
from visitor import AbstractVisitor

bytecode = {
    "halt": b"\x00",
    "noop": b"\x01",

    "add": b"\x02",
    "sbt": b"\x03",
    "mul": b"\x04",
    "div": b"\x05",
    "mod": b"\x06",

    "jmp": b"\x0F",
    "jeq": b"\x10",
    "jne": b"\x11",
    "jlt": b"\x12",
    "jle": b"\x13",
    "jgt": b"\x14",
    "jge": b"\x15",
    "jeqz": b"\x16",
    "jnez": b"\x17",
    "jltz": b"\x18",
    "jlez": b"\x19",
    "jgtz": b"\x1A",
    "jgez": b"\x1B",

    "cns_i32": b"\x1D",

    "move": b"\x22",
    "print": b"\x23",
}


class AssemblerError(Exception):
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg


class AssemblerVisitor(AbstractVisitor):
    def assemble(self, node):
        return node.accept(self)

    def visit_program(self, program: Program):
        header = b"\xCA\x11\x15\x71"
        maj_ver = struct.pack("<H", 0)
        min_ver = struct.pack("<H", 4)

        entry_code = self.assemble(program.subs[0])
        other_code = b"".join([self.assemble(sub) for sub in program.subs[1:]])
        byte_code = entry_code + b"\x00" + other_code

        cns_size = struct.pack("<I", 0)
        ins_size = struct.pack("<I", len(byte_code))

        return header + maj_ver + min_ver + cns_size + ins_size + byte_code

    def visit_sub_stm(self, sub_stm: SubStm):
        return b"".join([self.assemble(statement) for statement in sub_stm.instructions])

    def visit_halt_ins(self, hlt_ins: HaltIns):
        return bytecode["halt"]

    def visit_noop_ins(self, nop_ins: NoopIns):
        return bytecode["noop"]

    def visit_cns_i32_ins(self, i32_ins: CnsI32Ins):
        return bytecode["cns_i32"] + self.assemble(i32_ins.dest) + \
               self.assemble(i32_ins.lit_i32)

    def visit_add_ins(self, add_ins: AddIns):
        return bytecode["add"] + self.assemble(add_ins.dest) + \
               self.assemble(add_ins.src0) + \
               self.assemble(add_ins.src1)

    def visit_sub_ins(self, sub_ins: SubIns):
        return bytecode["sbt"] + self.assemble(sub_ins.dest) + \
               self.assemble(sub_ins.src0) + \
               self.assemble(sub_ins.src1)

    def visit_mul_ins(self, mul_ins: MulIns):
        return bytecode["mul"] + self.assemble(mul_ins.dest) + \
               self.assemble(mul_ins.src0) + \
               self.assemble(mul_ins.src1)

    def visit_div_ins(self, div_ins: DivIns):
        return bytecode["div"] + self.assemble(div_ins.dest) + \
               self.assemble(div_ins.src0) + \
               self.assemble(div_ins.src1)

    def visit_mod_ins(self, mod_ins: ModIns):
        return bytecode["mod"] + self.assemble(mod_ins.dest) + \
               self.assemble(mod_ins.src0) + \
               self.assemble(mod_ins.src1)

    def visit_jmp_ins(self, jmp_ins: JmpIns):
        return bytecode["jmp"] + self.assemble(jmp_ins.at_location)

    def visit_jeq_ins(self, jeq_ins: JeqIns):
        return bytecode["jeq"] + self.assemble(jeq_ins.at_location) + \
               self.assemble(jeq_ins.src0) + \
               self.assemble(jeq_ins.src1)

    def visit_jne_ins(self, jne_ins: JneIns):
        return bytecode["jeq"] + self.assemble(jne_ins.at_location) + \
               self.assemble(jne_ins.src0) + \
               self.assemble(jne_ins.src1)

    def visit_jlt_ins(self, jlt_ins: JltIns):
        return bytecode["jlt"] + self.assemble(jlt_ins.at_location) + \
               self.assemble(jlt_ins.src0) + \
               self.assemble(jlt_ins.src1)

    def visit_jle_ins(self, jle_ins: JleIns):
        return bytecode["jle"] + self.assemble(jle_ins.at_location) + \
               self.assemble(jle_ins.src0) + \
               self.assemble(jle_ins.src1)

    def visit_jgt_ins(self, jgt_ins: JgtIns):
        return bytecode["jgt"] + self.assemble(jgt_ins.at_location) + \
               self.assemble(jgt_ins.src0) + \
               self.assemble(jgt_ins.src1)

    def visit_jge_ins(self, jge_ins: JgeIns):
        return bytecode["jge"] + self.assemble(jge_ins.at_location) + \
               self.assemble(jge_ins.src0) + \
               self.assemble(jge_ins.src1)

    def visit_jeqz_ins(self, jeqz_ins: JeqzIns):
        return bytecode["jeqz"] + self.assemble(jeqz_ins.at_location) + \
               self.assemble(jeqz_ins.src0)

    def visit_jnez_ins(self, jnez_ins: JnezIns):
        return bytecode["jnez"] + self.assemble(jnez_ins.at_location) + \
               self.assemble(jnez_ins.src0)

    def visit_jltz_ins(self, jltz_ins: JltzIns):
        return bytecode["jltz"] + self.assemble(jltz_ins.at_location) + \
               self.assemble(jltz_ins.src0)

    def visit_jlez_ins(self, jlez_ins: JlezIns):
        return bytecode["jlez"] + self.assemble(jlez_ins.at_location) + \
               self.assemble(jlez_ins.src0)

    def visit_jgtz_ins(self, jgtz_ins: JgtzIns):
        return bytecode["jgtz"] + self.assemble(jgtz_ins.at_location) + \
               self.assemble(jgtz_ins.src0)

    def visit_jgez_ins(self, jgez_ins: JgezIns):
        return bytecode["jgez"] + self.assemble(jgez_ins.at_location) + \
               self.assemble(jgez_ins.src0)

    def visit_move_ins(self, move_ins: MoveIns):
        return bytecode["move"] + self.assemble(move_ins.dest) + \
               self.assemble(move_ins.src0)

    def visit_print_ins(self, print_ins: PrintIns):
        return bytecode["print"] + self.assemble(print_ins.src0)

    def visit_register(self, reg: Register):
        return struct.pack("<B", reg.reg_num)

    def visit_lit_i32(self, lit_i32: LitI32):
        return struct.pack("<I", int(lit_i32.i32_tok.lexeme))

    def visit_label(self, label: Label):
        return b""

    def visit_at_location(self, at_location: AtLocation):
        return struct.pack("<b", at_location.address)
