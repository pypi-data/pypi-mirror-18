#include <stdlib.h>
#include "mar345.h"


mardata *_init_mar() {
    mardata *mar;

    mar = (mardata *)malloc(sizeof(mardata));
    if (mar) {
        mar->image = NULL;
        mar->n_pixels = 0;
        mar->dim1 = 0;
        mar->dim2 = 0;
    }
    return mar;
}


void _destroy_mar(mardata *mar) {
    if (mar && mar->image)
        free(mar->image);
    if (mar)
        free(mar);
}


static mardata *check_mem(char *mem, mardata *mar) {
    if (mem) {
        mar->image = (uint32_t *)mem;
        return mar;
    } else
        return NULL;
}

mardata *init_mar_mem(mardata *mar, size_t dim1, size_t dim2) {
    char *mem;

    if (!dim1 || !dim2 || !mar)
        return NULL;

    if (mar->dim1 == dim1 && mar->dim2 == dim2 && mar->image)
        return mar;

    mar->n_pixels = dim1 * dim2;
    mar->dim1 = dim1;
    mar->dim2 = dim2;

    if (!mar->image) {
        mem = malloc(mar->n_pixels * sizeof(uint32_t));
        return check_mem(mem, mar);
    } else {
        mem = realloc(mar->image, mar->n_pixels * sizeof(uint32_t));
        if (check_mem(mem, mar))
            return mar;
        else {
            free(mar->image);
            return NULL;
        }
    }
}


#define CCP4_PCK_BLOCK_HEADER_LENGTH 6
#define CCP4_PCK_BLOCK_HEADER_LENGTH_V2 8
static const uint32_t CCP4_PCK_ERR_COUNT[] = {1, 2, 4, 8, 16, 32, 64, 128};
static const uint32_t CCP4_PCK_BIT_COUNT[] = {0, 4, 5, 6, 7, 8, 16, 32};
static const uint8_t CCP4_PCK_MASK[] = {0x00, 0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3F, 0x7F, 0xFF};


static void ccp4_unpack_string(char *packed, mardata *mar) {
    uint8_t t_,t2,_conv;
    int32_t err_val, bit_offset, num_error, num_bits, read_bits, i, x4, x3, x2, x1;

    bit_offset = 0; i = 0; num_error = 0; num_bits = 0;
    t_ = (uint8_t)*packed++;
    while (i < mar->n_pixels){
        if (num_error == 0){
            if (bit_offset >= (8-CCP4_PCK_BLOCK_HEADER_LENGTH)){
                t2 = (uint8_t)*packed++;
                t_ = (t_ >> bit_offset) + ((uint8_t)t2 << (8-bit_offset));
                num_error = CCP4_PCK_ERR_COUNT[t_ & CCP4_PCK_MASK[3]];
                num_bits = CCP4_PCK_BIT_COUNT[(t_>>3) & CCP4_PCK_MASK[3]];
                bit_offset = CCP4_PCK_BLOCK_HEADER_LENGTH + bit_offset - 8;
                t_ = t2;
            } else {
                num_error = CCP4_PCK_ERR_COUNT[(t_ >> bit_offset) & CCP4_PCK_MASK[3]];
                num_bits = CCP4_PCK_BIT_COUNT[(t_ >> (3+bit_offset)) & CCP4_PCK_MASK[3]];
                bit_offset += CCP4_PCK_BLOCK_HEADER_LENGTH;
            }
        } else {
            while (num_error > 0) {
                err_val=0; read_bits=0;
                while (read_bits < num_bits){
                    if (bit_offset + (num_bits - read_bits) >= 8) {
                        _conv = (t_ >> bit_offset) & CCP4_PCK_MASK[8-bit_offset];
                        err_val |= (uint32_t) _conv << read_bits;
                        read_bits += (8 - bit_offset);
                        bit_offset = 0;
                        t_= (uint8_t)*packed++;
                    } else {
                        _conv = (t_ >>bit_offset) & CCP4_PCK_MASK[num_bits-read_bits];
                        err_val |= _conv << read_bits;
                        bit_offset += (num_bits - read_bits);
                        read_bits = num_bits;
                    }

                }
                if (err_val & (1 << (num_bits - 1))) {
                    err_val |= -1 << (num_bits - 1);
                }
                if (i > mar->dim1) {
                    x4 = (int16_t)mar->image[i-1];
                    x3 = (int16_t)mar->image[i-mar->dim1+1];
                    x2 = (int16_t)mar->image[i-mar->dim1];
                    x1 = (int16_t)mar->image[i-mar->dim1-1];
                    mar->image[i] = (uint16_t)(err_val + (x4 + x3 + x2 + x1 + 2) / 4);
                } else if (i) {
                    mar->image[i] = (uint16_t)(err_val + mar->image[i-1]);
                } else {
                    mar->image[i] = (uint16_t) err_val;
                }
                i++;
                num_error--;
            }
        }
    }
}


static void handle_overflow_pixels(int32_t of, char *oft, mardata *mar) {
    uint32_t address, value;
    int32_t *overflow;

    overflow = (int32_t *)oft;
    while (of > 0) {
        address = overflow[2*of-2];
        if (address) {
            value = overflow[2*of-1];
            mar->image[address-1] = value;
        }
        of--;
    }
}


void decode_mar_image(char *packed, int32_t of, char *oft, mardata *mar) {
    ccp4_unpack_string(packed, mar);
    handle_overflow_pixels(of, oft, mar);
}
