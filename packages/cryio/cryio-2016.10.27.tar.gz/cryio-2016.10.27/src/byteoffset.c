#include <stdlib.h>
#include "cryio.h"
#include "byteoffset.h"



void decode_byte_offset(char *cbf, cbfdata *out) {
    int8_t delta8;
    int16_t delta16;
    int32_t pixel, *array;
    size_t i;

    pixel = 0;
    array = (int32_t *)out->mem;
    for (i=0; i<out->n_pixels; ++i) {
        delta8 = *cbf++;
        if ((delta8 & 0xff) == 0x80) {
            delta16 = *(int16_t *)cbf;
            cbf += 2;
            if ((delta16 & 0xffff) == 0x8000) {
                pixel += *(int32_t *)cbf;
                cbf += 4;
            } else {
                pixel += delta16;
            }
        } else {
            pixel += delta8;
        }
        *array++ = pixel;
    }
}


size_t encode_byte_offset(int32_t *array, cbfdata *out) {
    size_t i;
    int32_t diff, nval, cval;
    memptr t;

    cval = 0;
    t._8 = out->mem;
    for (i=0; i<out->n_pixels; ++i) {
        nval = *array++;
        diff = nval - cval;
        if (abs(diff) < 0x80) {
            *t._8++ = (char)diff;
        } else {
            *t._8++ = 0x80;
            if (abs(diff) < 0x8000) {
                *t._16++ = (int16_t)diff;
            } else {
                *t._16++ = 0x8000;
                *t._32++ = diff;
            }
        }
        cval = nval;
    }
    return t._8 - out->mem;
}


static cbfdata *check_mem(char *mem, cbfdata *cbf) {
    if (mem) {
        cbf->mem = (int8_t *)mem;
        return cbf;
    } else
        return NULL;
}


cbfdata *init_cbf_mem(cbfdata *cbf, size_t n_pixels) {
    char *mem;

    if (!n_pixels || !cbf)
        return NULL;

    if (n_pixels <= cbf->n_pixels && cbf->mem)
        return cbf;

    cbf->n_pixels = n_pixels;
    if (!cbf->mem) {
        mem = malloc(n_pixels * sizeof(int32_t));
        return check_mem(mem, cbf);
    } else {
        mem = realloc(cbf->mem, n_pixels * sizeof(int32_t));
        if (check_mem(mem, cbf))
            return cbf;
        else {
            free(cbf->mem);
            return NULL;
        }
    }
}


cbfdata *_init_cbf() {
    cbfdata *cbf;

    cbf = (cbfdata *)malloc(sizeof(cbfdata));
    if (cbf) {
        cbf->mem = NULL;
        cbf->n_pixels = 0;
    }
    return cbf;
}


void _destroy_cbf(cbfdata *cbf) {
    if (cbf && cbf->mem)
        free(cbf->mem);
    if (cbf)
        free(cbf);
}
