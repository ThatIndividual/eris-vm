#include <inttypes.h>

#ifndef ERIS_OBJ_H
#define ERIS_OBJ_H

struct obj {
     uint8_t *cns;
     uint8_t *ins;
    struct {
        uint8_t magic_number[4];
        uint16_t maj_ver;
        uint16_t min_ver;
        uint32_t cns_size;
        uint32_t ins_size;
    } header;
};

struct obj *Obj_read(const char *filename);
      void  Obj_dump(struct obj *obj);

#endif /* ERIS_OBJ_H */