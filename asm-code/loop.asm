sub main(args=0, locs=2) do
    i32 10 r0
    i32 1 r1
step:
    print r0
    sub r0 r1 r0
    jgtz @step r0
end