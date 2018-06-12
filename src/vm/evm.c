#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "evm.h"

struct evm *Evm_new()
{
    struct evm *evm = malloc(sizeof(struct evm));

    evm->ip = 0;
    evm->exec_stack_cap = 1024 * 1024;
    evm->exec_stack = malloc(evm->exec_stack_cap);
    if (evm->exec_stack) {
        evm->exec_stack_start = evm->exec_stack + evm->exec_stack_cap;
        // Move the fp and sp 5 and 7 registers in
        evm->sp = evm->exec_stack_start - (7 * 4);
        evm->fp = evm->exec_stack_start - (5 * 4);

        return evm;
    }
    else {
        puts("Could not allocate stack");
        exit(0);
    }
}
