sub main(args=0, locs=3) do
    i32 2 r0
    i32 8 r1

    add.i32 r0 r1 r2
    print r2
    sub.i32 r0 r1 r2
    print r2
    mul.i32 r0 r1 r2
    print r2
    div.i32 r1 r0 r2
    print r2

    i32 6 r0
    i32 120 r1
    mul.i32 r0 r1 r2
    print r2

    i32 -10 r0
    i32 -5 r1
    add.i32 r0 r1 r2
    print r2

    halt
end
