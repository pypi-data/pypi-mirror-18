#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include "ccp4.h"


#ifndef M_PI
    #define M_PI ((float)(3.14159265358979323846))
#endif
#define D2R ((float)(M_PI / 180.0))
#define UB_BUF sizeof(float) * 3 * 3
#define ALPHA 90.0f
#define S 10.0f
// unknown parameters from Bosak
#define kxC 0.0f
#define kyC 0.0f
#define kzC 0.0f



static void minvert3x3(float in[3][3], float out[3][3]) {
    size_t i, j;
    float det;

    det = 0;
    for(i=0; i<3; ++i)
        det += in[0][i] * (
            in[1][(i+1) % 3] * in[2][(i+2) % 3] -
            in[1][(i+2) % 3] * in[2][(i+1) % 3]
        );

    for(i=0; i<3; ++i)
        for(j=0; j<3; ++j)
           out[j][i] = (
               (in[(i+1) % 3][(j+1) % 3] * in[(i+2) % 3][(j+2) % 3]) -
               (in[(i+1) % 3][(j+2) % 3] * in[(i+2) % 3][(j+1) % 3])
           ) / det;
}


static void mmult3x3(float in1[3][3], float in2[3][3], float out[3][3]) {
    size_t i, j, t;

    for (i=0; i<3; ++i)
        for (j=0; j<3; ++j) {
            out[i][j] = 0.0;
            for (t=0; t<3; ++t)
                out[i][j] += in1[i][t] * in2[t][j];
        }
}


static void calc_cell(geometry *geo) {
    float ca, cb, cg, sg;

    ca = cosf(geo->par->cell_alpha);
    cb = cosf(geo->par->cell_beta);
    cg = cosf(geo->par->cell_gamma);
    sg = sinf(geo->par->cell_gamma);
    geo->mtx->cell[0][0] = geo->par->cell_a;
    geo->mtx->cell[0][1] = geo->par->cell_b * cg;
    geo->mtx->cell[0][2] = geo->par->cell_c * cb;
    geo->mtx->cell[1][0] = 0;
    geo->mtx->cell[1][1] = geo->par->cell_b * sg;
    geo->mtx->cell[1][2] = -geo->par->cell_c * (cb * cg - ca) / sg;
    geo->mtx->cell[2][0] = 0;
    geo->mtx->cell[2][1] = 0;
    geo->mtx->cell[2][2] = geo->par->cell_c * sqrtf(sg * sg - cb * cb - ca * ca + 2 * cb * cg * ca) / sg;
}


static void calc_b(geometry *geo) {
    minvert3x3(geo->mtx->cell, geo->mtx->b);
}


static void calc_u(geometry *geo) {
    size_t i, j;

    mmult3x3(geo->mtx->ub, geo->mtx->cell, geo->mtx->u);
    for(i=0; i<3; ++i)
        for(j=0; j<3; ++j)
            geo->mtx->u[i][j] /= geo->par->wavelength;
}


static void calc_g(geometry *geo) {
    int h0, h1, k0, k1, l0, l1;
    float a[3], b[3], c[3], absa, absc;

    h0 = 1; k0 = 0; l0 = 0;
    h1 = 0; k1 = 1; l1 = 0;

    a[0] = geo->mtx->b[0][0] * h0 + geo->mtx->b[0][1] * k0 + geo->mtx->b[0][2] * l0;
    a[1] = geo->mtx->b[1][0] * h0 + geo->mtx->b[1][1] * k0 + geo->mtx->b[1][2] * l0;
    a[2] = geo->mtx->b[2][0] * h0 + geo->mtx->b[2][1] * k0 + geo->mtx->b[2][2] * l0;

    b[0] = geo->mtx->b[0][0] * h1 + geo->mtx->b[0][1] * k1 + geo->mtx->b[0][2] * l1;
    b[1] = geo->mtx->b[1][0] * h1 + geo->mtx->b[1][1] * k1 + geo->mtx->b[1][2] * l1;
    b[2] = geo->mtx->b[2][0] * h1 + geo->mtx->b[2][1] * k1 + geo->mtx->b[2][2] * l1;

    absa = sqrtf(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
    a[0] /= absa; a[1] /= absa; a[2] /= absa;

    c[0] = a[1] * b[2] - a[2] * b[1];
    c[1] = a[2] * b[0] - a[0] * b[2];
    c[2] = a[0] * b[1] - a[1] * b[0];

    absc = sqrtf(c[0] * c[0] + c[1] * c[1] + c[2] * c[2]);
    c[0] /= absc; c[1] /= absc; c[2] /= absc;

    b[0] = c[1] * a[2] - c[2] * a[1];
    b[1] = c[2] * a[0] - c[0] * a[2];
    b[2] = c[0] * a[1] - c[1] * a[0];

    geo->mtx->g[0][0] = a[0]; geo->mtx->g[0][1] = a[1]; geo->mtx->g[0][2] = a[2];
    geo->mtx->g[1][0] = b[0]; geo->mtx->g[1][1] = b[1]; geo->mtx->g[1][2] = b[2];
    geo->mtx->g[2][0] = c[0]; geo->mtx->g[2][1] = c[1]; geo->mtx->g[2][2] = c[2];
}


static void calc_uu(geometry *geo) {
    size_t i, j, t;

    for (i=0; i<3; ++i)
        for (j=0; j<3; ++j) {
            geo->mtx->uu[i][j] = 0;
            for (t=0; t<3; ++t)
                geo->mtx->uu[i][j] += geo->mtx->g[i][t] * geo->mtx->u[j][t];
        }
}


static void calc_cell_matrices(geometry *geo) {
    memcpy(geo->mtx->ub, geo->par->ub, UB_BUF);
    geo->par->cell_alpha *= D2R;
    geo->par->cell_beta *= D2R;
    geo->par->cell_gamma *= D2R;
    calc_cell(geo);
    calc_b(geo);
    calc_u(geo);
    calc_g(geo);
    calc_uu(geo);
}


static void rot(float a[3][3], int index, float angle) {
    float _cos, _sin;

    memset(a, 0, UB_BUF);
    angle *= D2R;
    _cos = cosf(angle);
    _sin = sinf(angle);

    if (index == 1) {
        a[0][0] = 1.0f;
        a[1][1] = _cos;
        a[2][2] = _cos;
        a[1][2] = _sin;
        a[2][1] = -_sin;
    }
    else if (index == 2) {
        a[1][1] = 1.0f;
        a[0][0] = _cos;
        a[2][2] = _cos;
        a[0][2] = -_sin;
        a[2][0] = _sin;
    }
    else if (index == 3) {
        a[2][2] = 1.0f;
        a[1][1] = _cos;
        a[0][0] = _cos;
        a[0][1] = _sin;
        a[1][0] = -_sin;
    }
}


static void rotdet(geometry *geo, float a[3][3]) {
    float b[3][3], c[3][3];

    rot(b, 2, geo->par->d2);
    rot(c, 1, geo->par->d1);
    mmult3x3(b, c, a);
    memcpy(c, a, UB_BUF);
    rot(b, 3, geo->par->theta0);
    mmult3x3(b, c, a);
}


static void sphere_crysalis(geometry *geo) {
    size_t i;
    float itmp, jtmp, x, y, ts, px, py, pz, a[3][3], b[3][3], d2, d3, x2, y2, al;

    rotdet(geo, a);
    rot(b, 2, geo->par->b2);

    d2 = powf(geo->par->distance, 2);
    d3 = powf(geo->par->distance, 3);
    for(i=0; i<geo->s_array; ++i) {
        jtmp = floorf((float)i / (float)geo->par->inhor);
        itmp = i - geo->par->inhor * jtmp;
        itmp = geo->par->inhor - itmp - geo->par->yc - 1.0f;
        jtmp = geo->par->inver - jtmp - geo->par->xc - 1.0f;
        x = jtmp * geo->par->pixel;
        y = itmp * geo->par->pixel;
        x2 = powf(x, 2);
        y2 = powf(y, 2);
        al = d2 + x2 + y2;
        geo->lorentz[i] = powf(al, 2) * sqrtf(al) / d3 / (d2 + y2);
        px = -a[0][0] * geo->par->distance + a[0][1] * x + a[0][2] * y;
        py = -a[1][0] * geo->par->distance + a[1][1] * x + a[1][2] * y;
        pz = -a[2][0] * geo->par->distance + a[2][1] * x + a[2][2] * y;
        ts = sqrtf(px * px + py * py + pz * pz);
        geo->kxA[i] = 0.5f * (px / ts + b[0][0]) / geo->par->wavelength;
        geo->kyA[i] = 0.5f * (py / ts + b[1][0]) / geo->par->wavelength;
        geo->kzA[i] = 0.5f * (pz / ts + b[2][0]) / geo->par->wavelength;
    }
}


void ccp4_add_array(geometry *geo, int32_t *array, float angle, float osc) {
    size_t i, j, k, l, t;
    int32_t nx, ny, nz;
    float intensity, kx, ky, kz, a[3][3], b[3][3];

    for(t=0; t<geo->par->downsample; ++t) {
        rot(a, 3, angle + osc * ((t + 0.5f) / geo->par->downsample / D2R));
        for (i=0; i<3; ++i)
            for (j=0; j<3; ++j) {
                b[i][j] = 0;
                for (k=0; k<3; ++k)
                    b[i][j] += geo->mtx->uu[i][k] * a[j][k];
            }

        for(i=0; i<geo->s_array; ++i) {
            kx = geo->kxA[i] * b[0][0] + geo->kyA[i] * b[0][1] + geo->kzA[i] * b[0][2];
            ky = geo->kxA[i] * b[1][0] + geo->kyA[i] * b[1][1] + geo->kzA[i] * b[1][2];
            kz = geo->kxA[i] * b[2][0] + geo->kyA[i] * b[2][1] + geo->kzA[i] * b[2][2];

            nx = (int32_t)floorf(geo->par->x * (kx - kxC) / (2 * geo->par->dQ)) + geo->par->x / 2;
            ny = (int32_t)floorf(geo->par->y * (ky - kyC) / (2 * geo->par->dQ)) + geo->par->y / 2;
            nz = (int32_t)floorf(geo->par->z * (kz - kzC) / (2 * geo->par->dQ)) + geo->par->z / 2;
            intensity = (float)array[i];
            if ((intensity >= 0) && (nx >= 0) && (ny >= 0) && (nz >= 0) &&
                (nx < geo->par->x) && (ny < geo->par->y) && (nz < geo->par->z)) {
                l = (size_t)(nx * geo->par->y * geo->par->z + ny * geo->par->z + nz);
                if (geo->par->lorentz)
                    intensity *= geo->lorentz[i];
                geo->voxval[l] += intensity;
                geo->voxcount[l]++;
            }
        }
    }
}


static void ccp4_header(geometry *geo) {
    geo->ccp4_hdr->nc = geo->par->x;
    geo->ccp4_hdr->nr = geo->par->y;
    geo->ccp4_hdr->ns = geo->par->z;
    geo->ccp4_hdr->mode = 2;
    geo->ccp4_hdr->nx = geo->par->x;
    geo->ccp4_hdr->ny = geo->par->y;
    geo->ccp4_hdr->nz = geo->par->z;
    geo->ccp4_hdr->xlen = S;
    geo->ccp4_hdr->ylen = S;
    geo->ccp4_hdr->zlen = S;
    geo->ccp4_hdr->alpha = ALPHA;
    geo->ccp4_hdr->beta = ALPHA;
    geo->ccp4_hdr->gamma = ALPHA;
    geo->ccp4_hdr->mapc = 1;
    geo->ccp4_hdr->mapr = 2;
    geo->ccp4_hdr->maps = 3;
}


static void destroy_aux(geometry *geo) {
    if (geo != NULL) {
        if (geo->lorentz != NULL) {
            free(geo->lorentz);
            geo->lorentz = NULL;
        }
        if (geo->voxval != NULL) {
            free(geo->voxval);
            geo->voxval = NULL;
        }
        if (geo->voxcount != NULL) {
            free(geo->voxcount);
            geo->voxcount = NULL;
        }
    }
}


void ccp4_map(geometry *geo) {
    size_t i, j, k, l;
    float avg;
    float *res;

    if (geo->map_calculated)
        return;

    res = geo->voxels;
    for(i=0; i<geo->par->x; ++i)
        for(j=0; j<geo->par->y; ++j)
            for(k=0; k<geo->par->z; ++k) {
                l = i * geo->par->y * geo->par->z + j * geo->par->z + k;
                if (geo->voxval[l] > 0 && geo->voxcount[l] > 0) {
                    avg = geo->voxval[l] / geo->voxcount[l];
                    *res = (avg < 0xFFFFFF) ? avg : 0;
                }
                ++res;
            }
    geo->map_calculated = 1;
    destroy_aux(geo);
}


void _destroy_ccp4(geometry *geo) {
    destroy_aux(geo);
    if (geo != NULL) {
        if (geo->ccp4_hdr != NULL)
            free(geo->ccp4_hdr);
        free(geo);
    }
}


geometry *_init_ccp4(parfile *par) {
    geometry *geo;
    char *mem;

    mem = malloc(sizeof(geometry) + sizeof(cell_matrices));
    if (mem == NULL)
        return NULL;
    geo = (geometry *)mem;
    geo->mtx = (cell_matrices *)(geo + 1);
    geo->par = par;
    geo->map_calculated = 0;
    geo->s_array = geo->par->inhor * geo->par->inver;
    geo->s_buf = geo->s_array * sizeof(float);
    geo->s_voxels = geo->par->x * geo->par->y * geo->par->z;
    geo->s_output = sizeof(ccp4header) + geo->s_voxels * sizeof(float);

    geo->lorentz = NULL;
    geo->voxval = NULL;
    geo->voxcount = NULL;
    geo->ccp4_hdr = NULL;
    geo->voxels = NULL;

    geo->lorentz = malloc(geo->s_buf * 4);
    geo->voxval = calloc(geo->s_voxels, sizeof(float));
    geo->voxcount = calloc(geo->s_voxels, sizeof(float));
    geo->ccp4_hdr = malloc(geo->s_output);
    if (!geo->lorentz || !geo->voxval || !geo->voxcount || !geo->ccp4_hdr) {
        _destroy_ccp4(geo);
        return NULL;
    }
    memset(geo->ccp4_hdr, 0, geo->s_output);
    geo->voxels = (float *)(geo->ccp4_hdr + 1);

    geo->kxA = geo->lorentz + geo->s_array;
    geo->kyA = geo->kxA + geo->s_array;
    geo->kzA = geo->kyA + geo->s_array;

    ccp4_header(geo);
    calc_cell_matrices(geo);
    sphere_crysalis(geo);
    return geo;
}
