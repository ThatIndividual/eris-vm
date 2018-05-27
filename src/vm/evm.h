#include <inttypes.h>

#ifndef ERIS_EVM_H
#define ERIS_EVM_H

struct evm {
    uint32_t ip;
    uint32_t *reg;
    size_t reg_size;
};

struct evm *Evm_new();

#endif /* ERIS_EVM_H */
