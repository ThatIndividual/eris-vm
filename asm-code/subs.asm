sub main(args=0, locs=1) do
    i32 10 r0
    call quad r0
    receive r0
    print r0
    halt
end

sub quad(args=1, locs=0) do
    call double r0
    receive r0
    call double r0
    receive r0
    return r0
end

sub double(args=1, locs=0) do
    add.i32 r0 r0 r0
    return r0
end
