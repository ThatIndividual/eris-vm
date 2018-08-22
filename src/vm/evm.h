#ifndef ERIS_EVM_H
#define ERIS_EVM_H

#include <inttypes.h>

#include "value.h"

struct evm {
    struct obj *obj;
    uint32_t ip;
    uint32_t exec_stack_cap;
    void *exec_stack;
    void *exec_stack_start;
    void *sp;
    void *fp;
};

struct evm *Evm_new();

#endif /* ERIS_EVM_H */
