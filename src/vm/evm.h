#ifndef ERIS_EVM_H
#define ERIS_EVM_H

#include <inttypes.h>

struct evm {
    uint32_t ip;
    uint32_t *exec_stack;
    uint32_t *exec_stack_start;
    size_t exec_stack_cap;
    uint32_t *sp;
    uint32_t *fp;
};

struct evm *Evm_new();
void Evm_cs_grow(struct evm *evm);

#endif /* ERIS_EVM_H */
