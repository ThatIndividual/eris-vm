section entry do
    I32 r0 10
    I32 r1 1
    I32 r3 0
step:
    PRINT r0
    SUB r0 r0 r1
    JLT @step r3 r0
end