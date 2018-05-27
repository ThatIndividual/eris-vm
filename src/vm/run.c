#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"
#include "obj.h"
#include "ins.h"

void Evm_run_Obj(struct evm*, struct obj*);

int main(int argc, char *argv[])
{
//     int i;
//     for (i = 0; i < __N_INS; i++) {
//         printf("\"%s\": b\"\\x%02X\",\n", ins_label[i], i);
//     }

    if (argc == 2) {
        struct obj *obj = Obj_read(argv[1]);
        struct evm *evm = Evm_new(obj);

        Evm_run_Obj(evm, obj);
    }

    return 0;
}

void Evm_run_Obj(struct evm *evm, struct obj *obj)
{
    #define AS_DISPATCH(x, y) &&do_ ## y,
    #define DISPATCH() goto *dispatch_table[*ip++]
    #define R(x) (reg[(x)])
    static void *dispatch_table[] = { INS_TABLE(AS_DISPATCH) };

    /* used for moving bytes in and out of registers */
    uint32_t dest, src0, src1;
    int8_t adrs;

    /*
     * properties of either EVM or Obj that are demarshalled
     * inside the run loop
     */
    uint8_t *ip = obj->ins + evm->ip;
    uint32_t *reg = evm->reg;

    DISPATCH();

    do_halt:
        return;

    do_noop:
        DISPATCH();

    #define ARITH_I32(op) \
        do { \
            dest = *ip++; \
            src0 = *ip++; \
            src1 = *ip++; \
            R(dest) = R(src0) op R(src1); \
        } while(0)

    do_add_i32:
        ARITH_I32(+);
        DISPATCH();

    do_sub_i32:
        ARITH_I32(-);
        DISPATCH();

    do_mul_i32:
        ARITH_I32(*);
        DISPATCH();

    do_div_i32:
        ARITH_I32(/);
        DISPATCH();

    do_mod_i32:
        ARITH_I32(%);
        DISPATCH();

    #undef ARITH_I32

    do_jmp:
        adrs = *ip++;
        ip += adrs;
        DISPATCH();

    #define CMP_JMP(op) \
        do { \
            adrs = *ip++; \
            src0 = *ip++; \
            src1 = *ip++; \
            if (R(src0) op R(src1)) \
                ip += adrs; \
        } while(0);

    do_jmp_eq:
        CMP_JMP(==);
        DISPATCH();

    do_jmp_ne:
        CMP_JMP(!=);
        DISPATCH();

    do_jmp_lt:
        CMP_JMP(<)
        DISPATCH();

    do_jmp_le:
        CMP_JMP(<=);
        DISPATCH();

    do_jmp_gt:
        CMP_JMP(>);
        DISPATCH();

    do_jmp_ge:
        CMP_JMP(>=);
        DISPATCH();

    #undef CMP_JMP

    #define CMPZ_JMP(op) \
        do { \
            adrs = *ip++; \
            src0 = *ip++; \
            if (R(src0) op 0) \
                ip += adrs; \
        } while(0);

    do_jmp_eqz:
        CMPZ_JMP(==);
        DISPATCH();

    do_jmp_nez:
        CMPZ_JMP(!=);
        DISPATCH();

    do_jmp_ltz:
        CMPZ_JMP(<);
        DISPATCH();

    do_jmp_lez:
        CMPZ_JMP(<=);
        DISPATCH();

    do_jmp_gtz:
        CMPZ_JMP(>);
        DISPATCH();

    do_jmp_gez:
        CMPZ_JMP(>=);
        DISPATCH();

    #undef CMPZ_JMP

    do_cns_i32:
        dest = *ip++;
        R(dest) = *(uint32_t *)ip;
        ip += 4;
        DISPATCH();

    do_move:
        dest = *ip++;
        src0 = *ip++;
        R(dest) = R(src0);
        DISPATCH();

    do_print:
        src0 = *ip++;
        printf("%" PRIu32 "\n", R(src0));
        DISPATCH();

    /* unimplemented */
    do_add_flt: do_sub_flt: do_mul_flt: do_div_flt:
    do_i32_to_flt: do_flt_to_i32: do_call: do_ret:
    do_cns_chr: do_cns_flt: do_cns_str: do_load_glb: do_store_glb:
        return;

    #undef R
    #undef DISPATCH
    #undef AS_DISPATCH
}
