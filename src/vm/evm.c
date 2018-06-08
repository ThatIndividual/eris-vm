#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->ip = 0;
    evm->cs_len = 1024 * 1024;
    evm->cs = calloc(evm->cs_len, sizeof(uint32_t));
    evm->sp = evm->cs_len - 16;

    return evm;
}
