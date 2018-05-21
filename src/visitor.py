from abc import abstractmethod, ABC

from ast import *


class AbstractVisitor(ABC):
    @abstractmethod
    def visit_program(self, program: Program):
        pass

    @abstractmethod
    def visit_sub(self, sub_stm: SubStm):
        pass

    @abstractmethod
    def visit_hlt_ins(self, hlt_ins: HltIns):
        pass

    @abstractmethod
    def visit_nop_ins(self, nop_ins: NopIns):
        pass

    @abstractmethod
    def visit_cns_i32_ins(self, cns_i32_ins: CnsI32Ins):
        pass

    @abstractmethod
    def visit_add_ins(self, add_ins: AddIns):
        pass

    @abstractmethod
    def visit_sbt_ins(self, sub_ins: SbtIns):
        pass

    @abstractmethod
    def visit_mul_ins(self, mul_ins: MulIns):
        pass

    @abstractmethod
    def visit_div_ins(self, div_ins: DivIns):
        pass

    @abstractmethod
    def visit_mod_ins(self, mod_ins: ModIns):
        pass

    @abstractmethod
    def visit_jmp_ins(self, jmp_ins: JmpIns):
        pass

    @abstractmethod
    def visit_jeq_ins(self, jeq_ins: JeqIns):
        pass

    @abstractmethod
    def visit_jne_ins(self, jne_ins: JneIns):
        pass

    @abstractmethod
    def visit_jlt_ins(self, jlt_ins: JltIns):
        pass

    @abstractmethod
    def visit_jle_ins(self, jle_ins: JleIns):
        pass

    @abstractmethod
    def visit_jgt_ins(self, jgt_ins: JgtIns):
        pass

    @abstractmethod
    def visit_jge_ins(self, jge_ins: JgeIns):
        pass

    @abstractmethod
    def visit_jeqz_ins(self, jeqz_ins: JeqzIns):
        pass

    @abstractmethod
    def visit_jnez_ins(self, jnez_ins: JnezIns):
        pass

    @abstractmethod
    def visit_jltz_ins(self, jltz_ins: JltzIns):
        pass

    @abstractmethod
    def visit_jlez_ins(self, jlez_ins: JlezIns):
        pass

    @abstractmethod
    def visit_jgtz_ins(self, jgtz_ins: JgtzIns):
        pass

    @abstractmethod
    def visit_jgez_ins(self, jgez_ins: JgezIns):
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
