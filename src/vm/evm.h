#ifndef ERIS_EVM_H
#define ERIS_EVM_H

#include <inttypes.h>

struct evm {
    uint32_t ip;
    uint32_t *reg;
    size_t reg_len;
};

struct evm *Evm_new();
void Evm_reg_grow(struct evm *evm);

#endif /* ERIS_EVM_H */
