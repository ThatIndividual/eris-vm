import struct

from ast import *
from visitor import AbstractVisitor


class AssemblerError(Exception):
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg

class AssemblerVisitor(AbstractVisitor):
    def assemble(self, node):
        return node.accept(self)

    def visit_program(self, program: Program):
        header = b"KLST"
        maj_ver = struct.pack("<H", 0)
        min_ver = struct.pack("<H", 3)

        byte_code = b"".join([self.assemble(section)
                              for section in program.sections])

        cns_size = struct.pack("<I", 0)
        ins_size = struct.pack("<I", len(byte_code))

        return header + maj_ver + min_ver + cns_size + ins_size + byte_code

    def visit_section(self, section: Section):
        return b"".join([self.assemble(statement) for statement in section.instructions])

    def visit_cns_i32_ins(self, i32_ins: CnsI32Ins):
        return b"\x16" + self.assemble(i32_ins.dest) + \
               self.assemble(i32_ins.lit_i32)

    def visit_add_ins(self, add_ins: AddIns):
        return b"\x02" + self.assemble(add_ins.dest) + \
               self.assemble(add_ins.src0) + \
               self.assemble(add_ins.src1)

    def visit_sub_ins(self, sub_ins: AddIns):
        return b"\x03" + self.assemble(sub_ins.dest) + \
               self.assemble(sub_ins.src0) + \
               self.assemble(sub_ins.src1)

    def visit_mul_ins(self, mul_ins: AddIns):
        return b"\x04" + self.assemble(mul_ins.dest) + \
               self.assemble(mul_ins.src0) + \
               self.assemble(mul_ins.src1)

    def visit_div_ins(self, div_ins: AddIns):
        return b"\x05" + self.assemble(div_ins.dest) + \
               self.assemble(div_ins.src0) + \
               self.assemble(div_ins.src1)

    def visit_print_ins(self, print_ins: PrintIns):
        return b"\x1C" + self.assemble(print_ins.src0)

    def visit_jump_ins(self, jump_ins: JumpIns):
        return b"\x12" + self.assemble(jump_ins.at_location)

    def visit_jlt_ins(self, jump_lt_ins: JltIns):
        return b"\x14" + self.assemble(jump_lt_ins.at_location) + \
               self.assemble(jump_lt_ins.src0) + \
               self.assemble(jump_lt_ins.src1)

    def visit_register(self, reg: Register):
        return struct.pack("<B", reg.reg_num)

    def visit_lit_i32(self, lit_i32: LitI32):
        return struct.pack("<I", int(lit_i32.i32_tok.lexeme))

    def visit_label(self, label: Label):
        return b""

    def visit_at_location(self, at_location: AtLocation):
        return struct.pack("<b", at_location.address)
