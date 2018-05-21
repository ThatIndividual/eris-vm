ASM = ./src/asm.py

ASSEMBLY = arith fib gcd isPrime loop print42
AUR_TRG = $(addprefix obj/, $(addsuffix .aur, $(ASSEMBLY)))

default : gordias $(AUR_TRG)

gordias : gordias.c
	gcc gordias.c -o gordias

obj/%.aur : asm/%.asm
	$(ASM) $< $@
