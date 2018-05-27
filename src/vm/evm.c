#include <stdlib.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->reg = calloc(256, sizeof(uint32_t));
    evm->reg_size = 256;
    evm->ip = 0;

    return evm;
}