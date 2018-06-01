sub main(args=0, locs=4) do
    i32 r0 1299827
    i32 r1 2
    i32 r3 1
step:
    mod r2 r0 r1
    jeqz @end r2
    add r1 r1 r3
    jmp @step
end:
    print r1
end
