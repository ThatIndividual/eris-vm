#include <stdio.h>
#include <stdlib.h>

#include "common.h"
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

        Evm_run_Obj(evm, obj);
    }

    return 0;
}

void Evm_run_Obj(struct evm *evm, struct obj *obj)
{
    #define READ_INS_BYTE() *ip++
    #define AS_DISPATCH(x, y) &&do_ ## y,
    #define DISPATCH() goto *dispatch_table[READ_INS_BYTE()]
    #define VREG(x) (*(EVal *)(fp+((x)*VREG_SIZE)))
    static void *dispatch_table[] = { INS_TABLE(AS_DISPATCH) };

    uint32_t calls = 0;

    uint8_t src0, src1, dest;
    EVal ret;
    int8_t adrs;
    struct sub_desc sub;

    uint8_t *ip = obj->ins + evm->ip;
    void *sp = evm->sp;
    void *fp = evm->fp;

    DISPATCH();

    do_halt:
        printf("Calls done: %" PRIu32 "\n", calls);
        return;

    do_noop:
        DISPATCH();

    #define ARITH(op, type) \
        do { \
            src0 = READ_INS_BYTE(); \
            src1 = READ_INS_BYTE(); \
            dest = READ_INS_BYTE(); \
            VREG(dest).type = VREG(src0).type op VREG(src1).type; \
        } while(0)

    do_add_i32:
        ARITH(+, i);
        DISPATCH();

    do_sub_i32:
        ARITH(-, i);
        DISPATCH();

    do_mul_i32:
        ARITH(*, i);
        DISPATCH();

    do_div_i32:
        ARITH(/, i);
        DISPATCH();

    do_mod_i32:
        ARITH(%, i);
        DISPATCH();

    do_add_flt:
        ARITH(+, f);
        DISPATCH();

    do_sub_flt:
        ARITH(-, f);
        DISPATCH();

    do_mul_flt:
        ARITH(*, f);
        DISPATCH();

    do_div_flt:
        ARITH(/, f);
        DISPATCH();

    #undef ARITH

    do_i32_to_flt:
        src0 = READ_INS_BYTE();
        dest = READ_INS_BYTE();
        VREG(dest).f = (flt)VREG(src0).i;

    do_flt_to_i32:
        return;

    do_call:
        calls++;
        src0 = READ_INS_BYTE(); // sub index
        src1 = READ_INS_BYTE(); // number of arguments
        sub = obj->subs[src0];

        for (; src1 != 0; src1--) {
            ret = VREG(READ_INS_BYTE());
            ((EVal *)(sp -= VREG_SIZE))->i = ret.i;
        }

        sp -= (sub.locs * VREG_SIZE);

        ((EVal *)(sp -= VREG_SIZE))->i = ip-obj->ins;
        ((EVal *)(sp -= VREG_SIZE))->i = evm->exec_stack_start - fp;

        fp = sp + (2 * VREG_SIZE);
        ip = obj->ins + sub.address;
        DISPATCH();

    do_receive:
        src0 = READ_INS_BYTE();
        VREG(src0) = ret;
        DISPATCH();

    do_return:
        src0 = READ_INS_BYTE();
        ret = VREG(src0);
        /* FALLTHROUGH */

    do_return_nil:
        fp = evm->exec_stack_start - ((EVal *)sp)->i;
        sp += VREG_SIZE;

        ip = obj->ins + ((EVal *)sp)->i;
        sp += VREG_SIZE;

        sp = fp - (2 * VREG_SIZE);
        DISPATCH();

    do_jmp:
        adrs = READ_INS_BYTE();
        ip += adrs;
        DISPATCH();

    #define CMP_JMP(op) \
        do { \
            adrs = READ_INS_BYTE(); \
            src0 = READ_INS_BYTE(); \
            src1 = READ_INS_BYTE(); \
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
            adrs = READ_INS_BYTE(); \
            src0 = READ_INS_BYTE(); \
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
        src0 = READ_INS_BYTE();
        dest = READ_INS_BYTE();
        VREG(dest) = VREG(src0);
        DISPATCH();

    do_print:
        src0 = READ_INS_BYTE();
        printf("%" PRIi32 "\n", VREG(src0).i);
        DISPATCH();

    /* unimplemented */
    do_cns_chr: do_cns_flt: do_cns_str: do_load_glb: do_store_glb:
        return;

    #undef V
    #undef DISPATCH
    #undef AS_DISPATCH
}
