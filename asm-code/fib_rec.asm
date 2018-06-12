sub main(args=0, locs=4) do
    i32 0 r0
    i32 1 r1
    i32 40 r2

loop:
    call fib r0
    receive r3
    print r3
    add r0 r1 r0
    jlt @loop r0 r2
    halt
end

sub fib(args=1, locs=4) do
    i32 1 r1

    jle @trivial r0 r1
    sub r0 r1 r2
    call fib r2
    receive r3

    sub r2 r1 r2
    call fib r2
    receive r4

    add r3 r4 r4
    return r4
trivial:
    return r0
end