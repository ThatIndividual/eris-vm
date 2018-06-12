#ifndef ERIS_OBJ_H
#define ERIS_OBJ_H

#include <inttypes.h>

struct sub_desc {
    uint32_t address;
    uint16_t args;
    uint16_t locs;
};

struct obj {
    struct sub_desc *subs;
    uint8_t *ins;
    struct {
        uint8_t magic_number[4];
        uint16_t maj_ver;
        uint16_t min_ver;
        uint32_t sub_size;
        uint32_t ins_size;
    } header;
};

struct obj *Obj_read(const char *filename);
      void  Obj_dump(struct obj *obj);

#endif /* ERIS_OBJ_H */
