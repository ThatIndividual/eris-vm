class ProgramAst:
    def __init__(self, sections):
        self.sections = sections

    def accept(self, visitor):
        return visitor.visit_program(self)


class Section:
    def __init__(self, id, instructions):
        self.id = id
        self.instructions = instructions

    def accept(self, visitor):
        return visitor.visit_section(self)


class I32Ins:
    def __init__(self, dest, src0):
        self.dest = dest
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_i32_ins(self)


class AddIns:
    def __init__(self, dest, src0, src1):
        self.dest = dest
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_add_ins(self)


class SubIns:
    def __init__(self, dest, src0, src1):
        self.dest = dest
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_sub_ins(self)


class MulIns:
    def __init__(self, dest, src0, src1):
        self.dest = dest
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_mul_ins(self)


class DivIns:
    def __init__(self, dest, src0, src1):
        self.dest = dest
        self.src0 = src0
        self.src1 = src1

    def accept(self, visitor):
        return visitor.visit_div_ins(self)


class PrintIns:
    def __init__(self, src0):
        self.src0 = src0

    def accept(self, visitor):
        return visitor.visit_print_ins(self)


class I32Cons:
    def __init__(self, i32_tok):
        self.i32_tok = i32_tok

    def accept(self, visitor):
        return visitor.visit_i32_cons(self)


class Register:
    def __init__(self, reg_num: int):
        self.reg_num = reg_num

    def accept(self, visitor):
        return visitor.visit_register(self)
