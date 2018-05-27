#ifndef ERIS_INS_H
#define ERIS_INS_H

#define INS_TABLE(X) \
    X(HALT, halt) \
    X(NOOP, noop) \
    X(ADD_I32, add_i32) \
    X(SUB_I32, sub_i32) \
    X(MUL_I32, mul_i32) \
    X(DIV_I32, div_i32) \
    X(MOD_I32, mod_i32) \
    X(ADD_FLT, add_flt) \
    X(SUB_FLT, sub_flt) \
    X(MUL_FLT, mul_flt) \
    X(DIV_FLT, div_flt) \
    X(I32_TO_FLT, i32_to_flt) \
    X(FLT_TO_I32, flt_to_i32) \
    X(CALL, call) \
    X(RET, ret) \
    X(JMP, jmp) \
    X(JMP_EQ, jmp_eq) \
    X(JMP_NE, jmp_ne) \
    X(JMP_LT, jmp_lt) \
    X(JMP_LE, jmp_le) \
    X(JMP_GT, jmp_gt) \
    X(JMP_GE, jmp_ge) \
    X(JMP_EQZ, jmp_eqz) \
    X(JMP_NEZ, jmp_nez) \
    X(JMP_LTZ, jmp_ltz) \
    X(JMP_LEZ, jmp_lez) \
    X(JMP_GTZ, jmp_gtz) \
    X(JMP_GEZ, jmp_gez) \
    X(CNS_CHR, cns_chr) \
    X(CNS_I32, cns_i32) \
    X(CNS_FLT, cns_flt) \
    X(CNS_STR, cns_str) \
    X(LOAD_GLB, load_glb) \
    X(STORE_GLB, store_glb) \
    X(MOVE, move) \
    X(PRINT, print)

#define AS_BARE(x, y) x ,
#define AS_STR(x, y) #y ,

enum ins { INS_TABLE(AS_BARE) NUM_INS};
char *ins_label[] = { INS_TABLE(AS_STR) };

#undef AS_STR
#undef AS_BARE

#endif /* ERIS_INS_H */