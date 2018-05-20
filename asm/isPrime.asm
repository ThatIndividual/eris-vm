section entry do
    i32 r0 67
    i32 r1 2
    i32 r3 0
    i32 r4 1
step:
    mod r2 r0 r1
    jeq @end r2 r3
    add r1 r1 r4
    jump @step
end:
    print r1
end
