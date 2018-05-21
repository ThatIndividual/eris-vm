from ast import *
from visitor import AbstractVisitor


class ResolverError(Exception):
    pass


class ResolverVisitor(AbstractVisitor):
    """
    When the VM executes an instruction from the JMP family it does so after
    reading the instruction and all its arguments. This is relevant when
    calculating jump offsets.
    """

    def __init__(self):
        self.local_address = 0
        self.labels = {}
        self.unresolved = []

    def resolve(self, node):
        node.accept(self)

    def visit_program(self, program: Program):
        for section in program.sections:
            self.resolve(section)

    def visit_sub_stm(self, sub_stm: SubStm):
        self.local_address = 0
        self.labels = {}
        self.unresolved = []

        for statement in sub_stm.instructions:
            self.resolve(statement)
        for at_location, at_address in self.unresolved:
            at_name = at_location.name
            if at_name in self.labels:
                at_location.address = self.labels[at_name] - at_address
            else:
                raise ResolverError("At-location references non-existing label")

    def visit_halt_ins(self, halt_ins: HaltIns):
        self.local_address += 1

    def visit_noop_ins(self, noop_ins: NoopIns):
        self.local_address += 1

    def visit_cns_i32_ins(self, cns_i32_ins: CnsI32Ins):
        self.local_address += 6

    def visit_add_ins(self, add_ins: AddIns):
        self.local_address += 4

    def visit_sub_ins(self, sub_ins: SubIns):
        self.local_address += 4

    def visit_mul_ins(self, mul_ins: MulIns):
        self.local_address += 4

    def visit_div_ins(self, div_ins: DivIns):
        self.local_address += 4

    def visit_mod_ins(self, mod_ins: ModIns):
        self.local_address += 4

    def visit_jmp_ins(self, jmp_ins: JmpIns):
        self.local_address += 2
        self.resolve(jmp_ins.at_location)

    def visit_jeq_ins(self, jeq_ins: JeqIns):
        self.local_address += 4
        self.resolve(jeq_ins.at_location)

    def visit_jne_ins(self, jne_ins: JneIns):
        self.local_address += 4
        self.resolve(jne_ins.at_location)

    def visit_jlt_ins(self, jlt_ins: JltIns):
        self.local_address += 4
        self.resolve(jlt_ins.at_location)

    def visit_jle_ins(self, jle_ins: JleIns):
        self.local_address += 4
        self.resolve(jle_ins.at_location)

    def visit_jgt_ins(self, jgt_ins: JgtIns):
        self.local_address += 4
        self.resolve(jgt_ins.at_location)

    def visit_jge_ins(self, jge_ins: JgeIns):
        self.local_address += 4
        self.resolve(jge_ins.at_location)

    def visit_jeqz_ins(self, jeqz_ins: JeqzIns):
        self.local_address += 3
        self.resolve(jeqz_ins.at_location)

    def visit_jnez_ins(self, jnez_ins: JnezIns):
        self.local_address += 3
        self.resolve(jnez_ins.at_location)

    def visit_jltz_ins(self, jltz_ins: JltzIns):
        self.local_address += 3
        self.resolve(jltz_ins.at_location)

    def visit_jlez_ins(self, jlez_ins: JlezIns):
        self.local_address += 3
        self.resolve(jlez_ins.at_location)

    def visit_jgtz_ins(self, jgtz_ins: JgtzIns):
        self.local_address += 3
        self.resolve(jgtz_ins.at_location)

    def visit_jgez_ins(self, jgez_ins: JgezIns):
        self.local_address += 3
        self.resolve(jgez_ins.at_location)

    def visit_move_ins(self, move_ins: MoveIns):
        self.local_address += 3

    def visit_print_ins(self, print_ins: PrintIns):
        self.local_address += 2

    def visit_lit_i32(self, lit_i32: LitI32):
        pass

    def visit_register(self, reg: Register):
        pass

    def visit_label(self, label: Label):
        if label.name not in self.labels:
            self.labels[label.name] = self.local_address
        else:
            raise ResolverError("Duplicate label declarations inside the same scope")

    def visit_at_location(self, at_location: AtLocation):
        self.unresolved.append((at_location, self.local_address))
