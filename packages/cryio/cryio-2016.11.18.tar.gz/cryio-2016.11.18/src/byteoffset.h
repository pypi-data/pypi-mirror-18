#ifndef CRYIO_BYTEOFFSET_H_   /* Include guard */
#define CRYIO_BYTEOFFSET_H_ 1

#include <stdlib.h>
#include "winshit.h"


typedef struct {
    size_t n_pixels;
    int8_t *mem;
} cbfdata;


void decode_byte_offset(char *c_cbf, cbfdata *out);

size_t encode_byte_offset(int32_t *array, cbfdata *out);

cbfdata *init_cbf_mem(cbfdata *cbf, size_t n_pixels);

cbfdata *_init_cbf();

void _destroy_cbf(cbfdata *cbf);

#endif
