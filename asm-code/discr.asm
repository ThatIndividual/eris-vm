sub main(args=0, locs=3) do
    i32 4 r0
    i32 25 r1
    i32 5 r2

    call discr r0 r1 r2
    receive r0
    print r0
    halt
end

sub discr(args=3, locs=1) do
    i32 4 r3

    mul.i32 r1 r1 r1
    mul.i32 r3 r0 r3
    mul.i32 r3 r2 r3
    sub.i32 r1 r3 r3

    return r3
end