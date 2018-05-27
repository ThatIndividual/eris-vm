sub main(args=0, locs=2) do
    i32 r0 10
    i32 r1 5
    call rectArea r0 r0
    print r0
end

sub rectArea(args=2, locs=1) do
    mul r2 r0 r1
    ret r2
end
