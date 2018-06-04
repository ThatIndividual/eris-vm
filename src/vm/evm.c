#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->ip = 0;
    evm->cs = calloc(256, sizeof(uint32_t));
    evm->cs_len = 256;

    return evm;
}
