/*
 * Gordias cpu
 * 17.apr.2018
 */
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

enum ins {
    HALT, NOOP,
    ADD_I32, SUB_I32, MUL_I32, DIV_I32, MOD_I32,
    ADD_FLT, SUB_FLT, MUL_FLT, DIV_FLT,
    I32_TO_FLT, FLT_TO_I32,
    CALL, RET,
    JMP,
    JMP_EQ, JMP_NE, JMP_LT, JMP_LE, JMP_GT, JMP_GE,
    JMP_EQZ, JMP_NEZ, JMP_LTZ, JMP_LEZ, JMP_GTZ, JMP_GEZ,
    CNS_CHR, CNS_I32, CNS_FLT, CNS_STR,
    LOAD_GLB, STORE_GLB, MOVE, PRINT, __N_INS
};

char *ins_label[] = {
    "halt", "noop",
    "add_i32", "sub_i32", "mul_i32", "div_i32", "mod_i32",
    "add_flt", "sub_flt", "mul_flt", "div_flt",
    "i32_to_flt", "flt_to_i32",
    "call", "ret",
    "jmp",
    "jeq", "jne", "jlt", "jle", "jgt", "jge",
    "jeqz", "jnez", "jltz", "jlez", "jgtz", "jgez",
    "cns_chr", "cns_i32", "cns_flt", "cns_str",
    "load_glb", "store_glb", "move", "print"
};

struct obj {
     uint8_t *cns;
     uint8_t *ins;
    struct {
         uint8_t magic_number[4];
        uint16_t maj_ver;
        uint16_t min_ver;
        uint32_t cns_size;
        uint32_t ins_size;
    } header;
};

struct cpu {
    /* call stack */
     uint8_t *ip;
     uint8_t *cns;
     uint8_t *ins;
    uint32_t *reg;
      size_t  cns_size;
      size_t  ins_size;
      size_t  reg_size;
};

struct obj *Obj_read(const char *filename);
      void  Obj_dump(struct obj *obj);

struct cpu *Cpu_new(struct obj *obj);
      void  Cpu_run(struct cpu *cpu);


int main(int argc, char *argv[])
{
//     int i;
//     for (i = 0; i < __N_INS; i++) {
//         printf("\"%s\": b\"\\x%02X\",\n", ins_label[i], i);
//     }

    if (argc == 2) {
        struct obj *obj = Obj_read(argv[1]);
        struct cpu *cpu = Cpu_new(obj);

        Cpu_run(cpu);
    }

    return 0;
}

struct obj *Obj_read(const char *filename)
{
    FILE *file = fopen(filename, "rb");

    /*
     * read header: magic number      , 4 bytes
     *              version number    , 4 bytes
     *              constant pool size, 4 bytes
     *              instruction size  , 4 bytes
     */
    struct obj *obj = malloc(sizeof(struct obj));
    fread(&obj->header, 1, 16, file);

    /* read constants */
    obj->cns = calloc(obj->header.cns_size, 1);
    fread(obj->cns, 1, obj->header.cns_size, file);

    /* read instructions */
    obj->ins = calloc(obj->header.ins_size, 1);
    fread(obj->ins, 1, obj->header.ins_size, file);

    return obj;
}

struct cpu *Cpu_new(struct obj *obj)
{
    struct cpu *cpu = malloc(sizeof(struct cpu));

    cpu->cns = obj->cns;
    cpu->ins = obj->ins;
    cpu->reg = calloc(256, sizeof(uint32_t));
    cpu->cns_size = obj->header.cns_size;
    cpu->ins_size = obj->header.ins_size;
    cpu->reg_size = 256;
    cpu->ip = cpu->ins;

    return cpu;
}

void Cpu_run(struct cpu *cpu)
{
    uint32_t dest, src0, src1;
    int8_t adrs;
    static void *dispatch_table[] = {
        &&do_halt, &&do_noop,
        &&do_add_i32, &&do_sub_i32, &&do_mul_i32, &&do_div_i32, &&do_mod_i32,
        &&do_add_flt, &&do_sub_flt, &&do_mul_flt, &&do_div_flt,
        &&do_i32_to_flt, &&do_flt_to_i32,
        &&do_call, &&do_ret,
        &&do_jmp,
        &&do_jmp_eq, &&do_jmp_ne, &&do_jmp_lt, &&do_jmp_le, &&do_jmp_gt, &&do_jmp_ge,
        &&do_jmp_eqz, &&do_jmp_nez, &&do_jmp_ltz, &&do_jmp_lez, &&do_jmp_gtz, &&do_jmp_gez,

        &&do_cns_chr, &&do_cns_i32, &&do_cns_flt, &&do_cns_str,
        &&do_load_glb, &&do_store_glb, &&do_move, &&do_print
    };
    #define DISPATCH() goto *dispatch_table[*cpu->ip++]
    #define R(x) (cpu->reg[(x)])

    DISPATCH();

    do_halt:
        return;
    
    do_noop:
        DISPATCH();

    #define ARITH_I32(op) \
        do { \
            dest = *cpu->ip++; \
            src0 = *cpu->ip++; \
            src1 = *cpu->ip++; \
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
        adrs = *cpu->ip++;
        cpu->ip += adrs;
        DISPATCH();

    #define CMP_JMP(op) \
        do { \
            adrs = *cpu->ip++; \
            src0 = *cpu->ip++; \
            src1 = *cpu->ip++; \
            if (R(src0) op R(src1)) \
                cpu->ip += adrs; \
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
            adrs = *cpu->ip++; \
            src0 = *cpu->ip++; \
            if (R(src0) op 0) \
                cpu->ip += adrs; \
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
        dest = *cpu->ip++;
        R(dest) = *(uint32_t *)cpu->ip;
        cpu->ip += 4;
        DISPATCH();

    do_move:
        dest = *cpu->ip++;
        src0 = *cpu->ip++;
        R(dest) = R(src0);
        DISPATCH();

    do_print:
        src0 = *cpu->ip++;
        printf("%" PRIu32 "\n", R(src0));
        DISPATCH();

    /* unimplemented */
    do_add_flt: do_sub_flt: do_mul_flt: do_div_flt:
    do_i32_to_flt: do_flt_to_i32: do_call: do_ret:
    do_cns_chr: do_cns_flt: do_cns_str: do_load_glb: do_store_glb:
        return;

    #undef R
    #undef DISPATCH
}
