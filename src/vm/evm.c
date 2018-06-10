#include <stdlib.h>
#include <inttypes.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->ip = 0;
    evm->exec_stack_cap = 1024 * 1024;
    evm->exec_stack = calloc(evm->exec_stack_cap, sizeof(uint32_t));
    evm->exec_stack_start = evm->exec_stack + evm->exec_stack_cap;
    evm->sp = evm->exec_stack_start - 7;
    evm->fp = evm->exec_stack_start - 5;

    return evm;
}
