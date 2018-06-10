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
//     for (i = 0; i < NUM_INS; i++) {
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
    #define P_STACK() printf("SP %p\nFP %p\n", sp, fp); for (uint32_t* pp = sp; pp != evm->exec_stack_start; pp++) printf("%p %" PRIu32 "\n", pp, *pp)
    #define P_INS() printf("[%s]\n", ins_label[*(ip)])

    #define AS_DISPATCH(x, y) &&do_ ## y,
    #define DISPATCH() goto *dispatch_table[*ip++]
    #define V(x) (*(fp+(x)))
    static void *dispatch_table[] = { INS_TABLE(AS_DISPATCH) };

    uint8_t src0, src1, dest, ret;
    int8_t adrs;
    uint32_t lit_u32;
    struct sub_desc sub;

    uint8_t *ip = obj->ins + evm->ip;
    uint32_t *sp = evm->sp;
    uint32_t *fp = evm->fp;

    DISPATCH();

    do_halt:
        return;

    do_noop:
        DISPATCH();

    #define ARITH_I32(op) \
        do { \
            src0 = *ip++; \
            src1 = *ip++; \
            dest = *ip++; \
            V(dest) = V(src0) op V(src1); \
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

    do_call:
        src0 = *ip++; // sub index
        src1 = *ip++; // number of arguments
        sub = obj->subs[src0];

        for (; src1 != 0; src1--) {
            dest = V(*ip++);
            *--sp = dest;
        }

        sp -= sub.locs;

        *--sp = ip-obj->ins;
        *--sp = evm->exec_stack_start - fp;

        fp = sp + 2;
        ip = obj->ins + sub.address;
        DISPATCH();

    do_receive:
        src0 = *ip++;
        V(src0) = ret;
        DISPATCH();

    do_return:
        src0 = *ip++;
        ret = V(src0);
        /* FALLTHROUGH */

    do_return_nil:
        fp = evm->exec_stack_start - *sp++;

        ip = obj->ins + *sp++;
        sp = fp - 2;
        DISPATCH();

    do_jmp:
        adrs = *ip++;
        ip += adrs;
        DISPATCH();

    #define CMP_JMP(op) \
        do { \
            adrs = *ip++; \
            src0 = *ip++; \
            src1 = *ip++; \
            if (V(src0) op V(src1)) \
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
            if (V(src0) op 0) \
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
        lit_u32 = *(uint32_t *)ip;
        ip += 4;
        dest = *ip++;
        V(dest) = lit_u32;
        DISPATCH();

    do_move:
        src0 = *ip++;
        dest = *ip++;
        V(dest) = V(src0);
        DISPATCH();

    do_print:
        src0 = *ip++;
        printf("%" PRIu32 "\n", V(src0));
        DISPATCH();

    /* unimplemented */
    do_add_flt: do_sub_flt: do_mul_flt: do_div_flt:
    do_i32_to_flt: do_flt_to_i32:
    do_cns_chr: do_cns_flt: do_cns_str: do_load_glb: do_store_glb:
        return;

    #undef V
    #undef DISPATCH
    #undef AS_DISPATCH
}
