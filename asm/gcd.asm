sub entry do
    i32 r0 54321
    i32 r1 9876
step:
    jeqz @end r1
    move r2 r0
    move r0 r1
    mod r1 r2 r1
    jmp @step
end:
    print r0
    halt
end
