#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->reg = calloc(256, sizeof(uint32_t));
    evm->reg_len = 256;

    return evm;
}
