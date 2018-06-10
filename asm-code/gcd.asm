sub main(args=0, locs=3) do
    i32 54321 r0
    i32 9876 r1
step:
    jeqz @end r1
    move r0 r2
    move r1 r0
    mod r2 r1 r1
    jmp @step
end:
    print r0
    halt
end
