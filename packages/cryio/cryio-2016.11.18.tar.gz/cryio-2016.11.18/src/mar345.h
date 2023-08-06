#ifndef CRYIO_MAR345_H_   /* Include guard */
#define CRYIO_MAR345_H_ 1

#include "winshit.h"


typedef struct {
    size_t n_pixels;
    size_t dim1;
    size_t dim2;
    size_t overflow;
    uint32_t *image;
} mardata;


mardata *_init_mar();

void _destroy_mar(mardata *mar);

mardata *init_mar_mem(mardata *mar, size_t dim1, size_t n_pixels);

void decode_mar_image(char *packed, int32_t of, char *oft, mardata *mar);

#endif  // CRYIO_MAR345_H_
