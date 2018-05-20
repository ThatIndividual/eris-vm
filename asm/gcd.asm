section entry do
    i32 r0 54321
    i32 r1 9876
    i32 r3 0
step:
    jeq @end r1 r3
    move r2 r0
    move r0 r1
    mod r1 r2 r1
    jump @step
end:
    print r0
end
