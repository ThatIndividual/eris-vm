sub entry do
    i32 r0 1000
    i32 r1 0
    i32 r2 1
step:
    add r3 r1 r2
    print r3
    move r1 r2
    move r2 r3
    jlt @step r3 r0
    hlt
end
