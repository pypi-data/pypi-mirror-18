#ifndef CRYIO_AGI_BITFIELD_H_   /* Include guard */
#define CRYIO_AGI_BITFIELD_H_ 1

#include <stdlib.h>
#include "winshit.h"


typedef struct {
    size_t n_pixels;
    size_t dim;
    int8_t *mem;
    int32_t *addrs;
} espdata;


size_t encode_agi_bitfield(int32_t *array, espdata *out);

espdata *init_esp_mem(espdata *esp, size_t n_pixels);

espdata *_init_esp();

void _destroy_esp(espdata *esp);

#endif  // CRYIO_AGI_BITFIELD_H_
