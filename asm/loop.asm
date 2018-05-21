sub entry do
    i32 r0 10
    i32 r1 1
step:
    print r0
    sbt r0 r0 r1
    jgtz @step r0
    hlt
end