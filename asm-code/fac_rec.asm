sub main(args=0, locs=4) do
    i32 0 r0
    i32 1 r1
    i32 10 r2

loop:
    call fac r0
    receive r3
    print r3
    add r0 r1 r0
    jlt @loop r0 r2
    halt
end

sub fac(args=1, locs=3) do
    i32 2 r1
    i32 1 r2

    jlt @trivial r0 r1
    sub r0 r2 r3
    call fac r3
    receive r3
    mul r0 r3 r3
    return r3
trivial:
    return r2
end
