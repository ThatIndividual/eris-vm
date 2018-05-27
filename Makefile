ASM = ./src/asm/asm.py

ASSEMBLY = arith fib gcd isPrime loop print42
AUR_TRG = $(addprefix aur-code/, $(addsuffix .aur, $(ASSEMBLY)))

default : gordias $(AUR_TRG)

gordias : src/vm/gordias.c
	gcc src/vm/gordias.c -o gordias

aur-code/%.aur : asm-code/%.asm
	$(ASM) $< $@
