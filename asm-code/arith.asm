sub main(args=0, locs=3) do
    i32 2 r0
    i32 8 r1

    add r0 r1 r2
    print r2
    sub r0 r1 r2
    print r2
    mul r0 r1 r2
    print r2
    div r1 r0 r2
    print r2

    i32 6 r0
    i32 120 r1
    mul r0 r1 r2
    print r2

    halt
end
