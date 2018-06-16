CC = gcc-8
CFLAGS = -O3 -fno-strict-aliasing

ASSEMBLER = ./src/asm/asm.py

CODE = arith discr fac_rec fib fib_rec gcd isPrime pdist subs
AUR_TRG = $(addprefix aur-code/, $(addsuffix .aur, $(CODE)))
VM_SRC = $(addprefix src/vm/, run.c evm.c obj.c)

default : eris $(AUR_TRG)

eris : $(VM_SRC)
	$(CC) $(VM_SRC) $(CFLAGS) -o eris

aur-code/%.aur : asm-code/%.asm
	$(ASSEMBLER) $< $@
