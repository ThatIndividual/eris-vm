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

    def visit_section(self, section: Section):
        self.local_address = 0
        self.labels = {}
        self.unresolved = []

        for statement in section.instructions:
            self.resolve(statement)
        for at_location, at_address in self.unresolved:
            at_name = at_location.name
            if at_name in self.labels:
                at_location.address = self.labels[at_name] - at_address
            else:
                raise ResolverError("At-location references non-existing label")

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

    def visit_jump_ins(self, jump_ins: JumpIns):
        self.local_address += 2
        self.resolve(jump_ins.at_location)

    def visit_jeq_ins(self, jeq_ins: JeqIns):
        self.local_address += 4
        self.resolve(jeq_ins.at_location)

    def visit_jlt_ins(self, jlt_ins: JltIns):
        self.local_address += 4
        self.resolve(jlt_ins.at_location)

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
