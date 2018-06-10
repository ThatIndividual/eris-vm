ASM = ./src/asm/asm.py

ASSEMBLY = arith fac_rec fib gcd isPrime loop print42 subs
AUR_TRG = $(addprefix aur-code/, $(addsuffix .aur, $(ASSEMBLY)))
VM_SRC = $(addprefix src/vm/, run.c evm.c obj.c)

default : eris $(AUR_TRG)

eris : $(VM_SRC)
	gcc $(VM_SRC) -O3 -o eris

aur-code/%.aur : asm-code/%.asm
	$(ASM) $< $@
