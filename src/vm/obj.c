#include <stdio.h>
#include <stdlib.h>

#include "obj.h"

struct obj *Obj_read(const char *filename)
{
    FILE *file = fopen(filename, "rb");

    /*
     * read header: magic number      , 4 bytes
     *              version number    , 4 bytes
     *              constant pool size, 4 bytes
     *              instruction size  , 4 bytes
     */
    struct obj *obj = malloc(sizeof(struct obj));
    fread(&obj->header, 1, 16, file);

    /* read constants */
    obj->subs = calloc(obj->header.sub_size, sizeof(struct sub_desc));
    fread(obj->subs, 8, obj->header.sub_size, file);

    /* read instructions */
    obj->ins = calloc(obj->header.ins_size, 1);
    fread(obj->ins, 1, obj->header.ins_size, file);

    return obj;
}