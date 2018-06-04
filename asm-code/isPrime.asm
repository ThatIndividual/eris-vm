sub main(args=0, locs=4) do
    i32 1299827 r0
    i32 2 r1
    i32 1 r3
step:
    mod r0 r1 r2
    jeqz @end r2
    add r1 r3 r1
    jmp @step
end:
    print r1
end
