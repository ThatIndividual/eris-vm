#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"
#include "obj.h"
#include "ins.h"
#include "value.h"

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

        puts("read object");

        Evm_run_Obj(evm, obj);
    }

    return 0;
}

void Evm_run_Obj(struct evm *evm, struct obj *obj)
{
    #define P_STACK() printf("SP %p\nFP %p\n", sp, fp); for (uint32_t* pp = sp; pp != evm->exec_stack_start; pp++) printf("%p %" PRIu32 "\n", pp, *pp)
    #define P_INS() printf("[%s]\n", ins_label[*(ip)])

    #define AS_DISPATCH(x, y) &&do_ ## y,
    #define DISPATCH() printf("[%s]\n", ins_label[*ip]); goto *dispatch_table[*ip++]
    #define VREG(x) (*(EVal *)(fp+((x)*4)))
    static void *dispatch_table[] = { INS_TABLE(AS_DISPATCH) };

    puts("entered run");

    uint32_t calls = 0;

    uint8_t src0, src1, dest;
    EVal ret;
    int8_t adrs;
    struct sub_desc sub;

    uint8_t *ip = obj->ins + evm->ip;
    void *sp = evm->sp;
    void *fp = evm->fp;

    printf("Before first dispatch, INS %p, IP %p\n", obj->ins, ip);

    DISPATCH();

    do_halt:
        printf("Calls done: %" PRIu32 "\n", calls);
        return;

    do_noop:
        DISPATCH();

    #define ARITH_I32(op) \
        do { \
            src0 = *ip++; \
            src1 = *ip++; \
            dest = *ip++; \
            VREG(dest).i = VREG(src0).i op VREG(src1).i; \
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
        calls++;
        src0 = *ip++; // sub index
        src1 = *ip++; // number of arguments
        sub = obj->subs[src0];

        for (; src1 != 0; src1--) {
            ret = VREG(*ip++);
            ((EVal *)(sp -= 4))->i = ret.i;
        }

        sp -= (sub.locs * 4);

        ((EVal *)(sp -= 4))->i = ip-obj->ins;
        ((EVal *)(sp -= 4))->i = evm->exec_stack_start - fp;

        fp = sp + (2 * 4);
        ip = obj->ins + sub.address;
        DISPATCH();

    do_receive:
        src0 = *ip++;
        VREG(src0) = ret;
        DISPATCH();

    do_return:
        src0 = *ip++;
        ret = VREG(src0);
        /* FALLTHROUGH */

    do_return_nil:
        fp = evm->exec_stack_start - ((EVal *)sp)->i;
        sp += 4;

        ip = obj->ins + ((EVal *)sp)->i;
        sp += 4;

        sp = fp - (2 * 4);
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
            if (VREG(src0).i op VREG(src1).i) \
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
            if (VREG(src0).i op 0) \
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
        VREG(*(ip+4)).i = *(int32_t *)ip;
        ip += 5;
        DISPATCH();

    do_move:
        src0 = *ip++;
        dest = *ip++;
        VREG(dest) = VREG(src0);
        DISPATCH();

    do_print:
        src0 = *ip++;
        printf("%" PRIi32 "\n", VREG(src0).i);
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
