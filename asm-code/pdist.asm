sub main(args=0, locs=4) do
    i32 2  r0
    i32 10 r1
    i32 3  r2
    i32 4  r3

    call pdist r0 r1 r2 r3
    receive r0

    print r0
    halt
end

sub pdist(args=4, locs=0) do
    sub.i32 r0 r1 r0
    mul.i32 r0 r0 r0
    sub.i32 r2 r3 r2
    mul.i32 r2 r2 r2
    add.i32 r0 r2 r0

    i32.flt r0 r0
    call sqrt r0
    receive r0
    return r0
end


sub sqrt(args=1, locs=5) do
    i32 1 r1
    i32 2 r2
    i32 1 r3
    i32 10 r4

    i32.flt r1 r1
    i32.flt r2 r2

loop:
    div.flt r0 r1 r5
    add.flt r5 r1 r5
    div.flt r5 r2 r1

    sub.i32 r4 r3 r4
    jgtz @loop r4

    return r1
end

