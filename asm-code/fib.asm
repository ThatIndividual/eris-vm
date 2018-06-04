sub main(args=0, locs=4) do
    i32 1000 r0
    i32 0 r1
    i32 1 r2
step:
    add r1 r2 r3
    print r3
    move r2 r1
    move r3 r2
    jlt @step r3 r0
end
