sub main(args=0, locs=2) do
    i32 10 r0
    i32 5 r1
    call rectArea r0 r0
    print r0
end

sub rectArea(args=2, locs=1) do
    mul r0 r1 r2
    ret r2
end
