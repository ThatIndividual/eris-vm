from abc import abstractmethod, ABC

from ast import *


class AbstractVisitor(ABC):
    @abstractmethod
    def visit_program(self, program: Program):
        pass

    @abstractmethod
    def visit_section(self, section: Section):
        pass

    @abstractmethod
    def visit_cns_i32_ins(self, cns_i32_ins: CnsI32Ins):
        pass

    @abstractmethod
    def visit_add_ins(self, add_ins: AddIns):
        pass

    @abstractmethod
    def visit_sub_ins(self, sub_ins: SubIns):
        pass

    @abstractmethod
    def visit_mul_ins(self, mul_ins: MulIns):
        pass

    @abstractmethod
    def visit_div_ins(self, div_ins: DivIns):
        pass

    @abstractmethod
    def visit_jump_ins(self, jump_ins: JumpIns):
        pass

    @abstractmethod
    def visit_jlt_ins(self, jlt_ins: JltIns):
        pass

    @abstractmethod
    def visit_jeq_ins(self, jeq_ins: JeqIns):
        pass

    @abstractmethod
    def visit_move_ins(self, move_ins: MoveIns):
        pass

    @abstractmethod
    def visit_print_ins(self, print_ins: PrintIns):
        pass

    @abstractmethod
    def visit_lit_i32(self, lit_i32: LitI32):
        pass

    @abstractmethod
    def visit_register(self, reg: Register):
        pass

    @abstractmethod
    def visit_label(self, label: Label):
        pass

    @abstractmethod
    def visit_at_location(self, at_location: AtLocation):
        pass


class BaseVisitor(AbstractVisitor):
    def visit_program(self, program: Program):
        for section in program.sections:
            section.accept(self)

    def visit_section(self, section: Section):
        for statement in section.instructions:
            statement.accept(self)

    def visit_cns_i32_ins(self, cns_i32_ins: CnsI32Ins):
        cns_i32_ins.dest.accept(self)
        cns_i32_ins.lit_i32.accept()

    def visit_add_ins(self, add_ins: AddIns):
        add_ins.dest.accept(self)
        add_ins.src0.accept(self)
        add_ins.src1.accept(self)

    def visit_sub_ins(self, sub_ins: SubIns):
        sub_ins.dest.accept(self)
        sub_ins.src0.accept(self)
        sub_ins.src1.accept(self)

    def visit_mul_ins(self, mul_ins: MulIns):
        mul_ins.dest.accept(self)
        mul_ins.src0.accept(self)
        mul_ins.src1.accept(self)

    def visit_div_ins(self, div_ins: DivIns):
        div_ins.dest.accept(self)
        div_ins.src0.accept(self)
        div_ins.src1.accept(self)

    def visit_print_ins(self, print_ins: PrintIns):
        print_ins.src0.accept(self)

    def visit_jump_ins(self, jump_ins: JumpIns):
        jump_ins.at_location.accept(self)

    def visit_jeq_ins(self, jeq_ins: JeqIns):
        jeq_ins.at_location.accept(self)
        jeq_ins.src0.accept(self)
        jeq_ins.src1.accept(self)

    def visit_jlt_ins(self, jlt_ins: JltIns):
        jlt_ins.at_location.accept(self)
        jlt_ins.src0.accept(self)
        jlt_ins.src1.accept(self)

    def visit_lit_i32(self, lit_i32: LitI32):
        pass

    def visit_register(self, reg: Register):
        pass

    def visit_label(self, label: Label):
        pass

    def visit_at_location(self, at_location: AtLocation):
        pass

