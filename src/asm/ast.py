class Program:
    def __init__(self, subs):
        self.subs = subs

    def accept(self, visitor):
        return visitor.visit_program(self)


class SubStm:
    def __init__(self, id, instructions, args, locs):
        self.id = id
        self.instructions = instructions
        self.args = args
        self.locs = locs
        self.address = None

    def accept(self, visitor):
        return visitor.visit_sub_stm(self)


class HaltIns:
    def accept(self, visitor):
        return visitor.visit_halt_ins(self)


class NoopIns:
    def accept(self, visitor):
        return visitor.visit_noop_ins(self)


class CnsI32Ins:
    def __init__(self, lit_i32, dest):
        self.lit_i32 = lit_i32
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_cns_i32_ins(self)


class AddI32Ins:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_add_i32_ins(self)


class SubI32Ins:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_sub_i32_ins(self)


class MulI32Ins:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_mul_i32_ins(self)


class DivI32Ins:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_div_i32_ins(self)


class ModI32Ins:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_mod_i32_ins(self)


class AddFltIns:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_add_flt_ins(self)


class SubFltIns:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_sub_flt_ins(self)


class MulFltIns:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_mul_flt_ins(self)


class DivFltIns:
    def __init__(self, src0, src1, dest):
        self.src0 = src0
        self.src1 = src1
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_div_flt_ins(self)


class I32FltIns:
    def __init__(self, src0, dest):
        self.src0 = src0
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_i32_flt_ins(self)


class FltI32Ins:
    def __init__(self, src0, dest):
        self.src0 = src0
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_flt_i32_ins(self)


class CallIns:
    def __init__(self, id, src):
        self.id = id
        self.sub = None
        self.src = src

    def accept(self, visitor):
        return visitor.visit_call_ins(self)


class ReceiveIns:
    def __init__(self, src):
        self.src = src

    def accept(self, visitor):
        return visitor.visit_receive_ins(self)


class RetIns:
    def __init__(self, src0):
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_ret_ins(self)


class JmpIns:
    def __init__(self, at_location):
        self.at_location = at_location

    def accept(self, visitor):
        return visitor.visit_jmp_ins(self)


class JeqIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jeq_ins(self)


class JneIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jne_ins(self)


class JltIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jlt_ins(self)


class JleIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jle_ins(self)


class JgtIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jgt_ins(self)


class JgeIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_jge_ins(self)


class JeqzIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jeqz_ins(self)


class JnezIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jnez_ins(self)


class JltzIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jltz_ins(self)


class JlezIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jlez_ins(self)


class JgtzIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jgtz_ins(self)


class JgezIns:
    def __init__(self, at_location, src0, src1):
        self.at_location = at_location
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_jgez_ins(self)


class MoveIns:
    def __init__(self, src0, dest):
        self.src0 = src0
        self.dest = dest

    def accept(self, visitor):
        return visitor.visit_move_ins(self)


class PrintIns:
    def __init__(self, src0):
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_print_ins(self)


class LitI32:
    def __init__(self, i32_tok):
        self.i32_tok = i32_tok

    def accept(self, visitor):
        return visitor.visit_lit_i32(self)


class Register:
    def __init__(self, reg_num: int):
        self.reg_num = reg_num

    def accept(self, visitor):
        return visitor.visit_register(self)


class Label:
    def __init__(self, lexeme: str):
        self.name = lexeme[:-1]

    def accept(self, visitor):
        return visitor.visit_label(self)


class AtLocation:
    def __init__(self, name):
        self.name = name
        self.address = None

    def accept(self, visitor):
        return visitor.visit_at_location(self)
