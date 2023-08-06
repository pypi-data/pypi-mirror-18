#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "ccp4.h"
#include "winshit.h"


#define D2R M_PI / 180.0
#define UB_BUF sizeof(double) * 3 * 3


static void minvert3x3(double in[3][3], double out[3][3]) {
    size_t i, j;
    double det;

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


static void mmult3x3(double in1[3][3], double in2[3][3], double out[3][3]) {
    size_t i, j, t;

    for (i=0; i<3; ++i)
        for (j=0; j<3; ++j) {
            out[i][j] = 0.0;
            for (t=0; t<3; ++t)
                out[i][j] += in1[i][t] * in2[t][j];
        }
}


static void calc_cell(geometry *geo) {
    geo->mtx->cell[0][0] = geo->par->cell_a;
    geo->mtx->cell[0][1] = geo->par->cell_b * cos(geo->par->cell_gamma);
    geo->mtx->cell[0][2] = geo->par->cell_c * cos(geo->par->cell_beta);
    geo->mtx->cell[1][0] = 0;
    geo->mtx->cell[1][1] = geo->par->cell_b * sin(geo->par->cell_gamma);
    geo->mtx->cell[1][2] = -geo->par->cell_c * (cos(geo->par->cell_beta) * cos(geo->par->cell_gamma) -
                                                cos(geo->par->cell_alpha)) / sin(geo->par->cell_gamma);
    geo->mtx->cell[2][0] = 0;
    geo->mtx->cell[2][1] = 0;
    geo->mtx->cell[2][2] = (geo->par->cell_c * sqrt(sin(geo->par->cell_gamma) * sin(geo->par->cell_gamma) -
                            cos(geo->par->cell_beta) *cos(geo->par->cell_beta) - cos(geo->par->cell_alpha)
                            * cos(geo->par->cell_alpha) + 2 * cos(geo->par->cell_beta)
                            * cos(geo->par->cell_gamma) * cos(geo->par->cell_alpha))
                            / sin(geo->par->cell_gamma));
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
    double a[3], b[3], c[3], absa, absc;

    h0 = 1; k0 = 0; l0 = 0;
    h1 = 0; k1 = 1; l1 = 0;

    a[0] = geo->mtx->b[0][0] * h0 + geo->mtx->b[0][1] * k0 + geo->mtx->b[0][2] * l0;
    a[1] = geo->mtx->b[1][0] * h0 + geo->mtx->b[1][1] * k0 + geo->mtx->b[1][2] * l0;
    a[2] = geo->mtx->b[2][0] * h0 + geo->mtx->b[2][1] * k0 + geo->mtx->b[2][2] * l0;

    b[0] = geo->mtx->b[0][0] * h1 + geo->mtx->b[0][1] * k1 + geo->mtx->b[0][2] * l1;
    b[1] = geo->mtx->b[1][0] * h1 + geo->mtx->b[1][1] * k1 + geo->mtx->b[1][2] * l1;
    b[2] = geo->mtx->b[2][0] * h1 + geo->mtx->b[2][1] * k1 + geo->mtx->b[2][2] * l1;

    absa = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
    a[0] /= absa; a[1] /= absa; a[2] /= absa;

    c[0] = a[1] * b[2] - a[2] * b[1];
    c[1] = a[2] * b[0] - a[0] * b[2];
    c[2] = a[0] * b[1] - a[1] * b[0];

    absc = sqrt(c[0] * c[0] + c[1] * c[1] + c[2] * c[2]);
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


void calc_cell_matrices(geometry *geo) {
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


static void rot(double a[3][3], int index, double angle) {
    double _cos, _sin;

    memset(a, 0, UB_BUF);
    angle *= D2R;
    _cos = cos(angle);
    _sin = sin(angle);

    if (index == 1) {
        a[0][0] = 1.0;
        a[1][1] = _cos;
        a[2][2] = _cos;
        a[1][2] = _sin;
        a[2][1] = -_sin;
    }
    else if (index == 2) {
        a[1][1] = 1.0;
        a[0][0] = _cos;
        a[2][2] = _cos;
        a[0][2] = -_sin;
        a[2][0] = _sin;
    }
    else if (index == 3) {
        a[2][2] = 1.0;
        a[1][1] = _cos;
        a[0][0] = _cos;
        a[0][1] = _sin;
        a[1][0] = -_sin;
    }
}


static void rotdet(geometry *geo, double a[3][3]) {
    double b[3][3], c[3][3];

    rot(b, 2, geo->par->d2);
    rot(c, 1, geo->par->d1);
    mmult3x3(b, c, a);
    memcpy(c, a, UB_BUF);
    rot(b, 3, geo->par->theta0);
    mmult3x3(b, c, a);
}


void sphere_crysalis(geometry *geo) {
    size_t i;
    double itmp, jtmp, x, y, ts, px, py, pz;
    double a[3][3], b[3][3];

    rotdet(geo, a);
    rot(b, 2, geo->par->b2);

    for(i=0; i<geo->s_array; ++i) {
        jtmp = floor((double)i / (double)geo->par->inhor);
        itmp = i - geo->par->inhor * jtmp;
        itmp = geo->par->inhor - itmp - geo->par->yc - 1.0;
        jtmp = geo->par->inver - jtmp - geo->par->xc - 1.0;
        x = jtmp * geo->par->pixel;
        y = itmp * geo->par->pixel;
        geo->lorentz[i] = (geo->par->distance * geo->par->distance + x * x + y * y)
                          * (geo->par->distance * geo->par->distance + x * x + y * y)
                          * sqrt(geo->par->distance * geo->par->distance + x * x + y * y)
                          / (geo->par->distance * geo->par->distance * geo->par->distance
                             * (geo->par->distance * geo->par->distance + y * y));
        px = -a[0][0] * geo->par->distance + a[0][1] * x + a[0][2] * y;
        py = -a[1][0] * geo->par->distance + a[1][1] * x + a[1][2] * y;
        pz = -a[2][0] * geo->par->distance + a[2][1] * x + a[2][2] * y;
        ts = sqrt(px * px + py * py + pz * pz);

        geo->kxA[i] = 0.5 * (px / ts + b[0][0]) / geo->par->wavelength;
        geo->kyA[i] = 0.5 * (py / ts + b[1][0]) / geo->par->wavelength;
        geo->kzA[i] = 0.5 * (pz / ts + b[2][0]) / geo->par->wavelength;
    }
}


// unknown parameters from Bosak
#define kxC 0
#define kyC 0
#define kzC 0

void cbf2ccp4(geometry *geo, double angle, double osc) {
    size_t i, j, t, k;
    int64_t nx, ny, nz;
    int32_t *array;
    double intensity, kx, ky, kz, a[3][3], b[3][3];

    array = (int32_t *)geo->cbf->mem;
    for(t=0; t<geo->par->downsample; ++t) {
        rot(a, 3, angle + osc * ((t + 0.5) / geo->par->downsample / D2R));

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

            nx = (int64_t)floor(geo->par->x * (kx - kxC) / (2 * geo->par->dQ)) + geo->par->x / 2;
            ny = (int64_t)floor(geo->par->y * (ky - kyC) / (2 * geo->par->dQ)) + geo->par->y / 2;
            nz = (int64_t)floor(geo->par->z * (kz - kzC) / (2 * geo->par->dQ)) + geo->par->z / 2;

            if ((array[i] >= 0) && (nx >= 0) && (ny >= 0) && (nz >= 0) &&
                (nx < geo->par->x) && (ny < geo->par->y) && (nz < geo->par->z)) {
                intensity = (double)(array[i]);
                if (geo->par->lorentz)
                    intensity *= geo->lorentz[i];
                geo->voxval[nx][ny][nz] += intensity;
                geo->voxcount[nx][ny][nz] += 1;
            }
        }
    }
}

void ccp4_map(geometry *geo) {
    size_t i, j, k;
    double avg;
    float *res;

    res = geo->voxels;
    for(i=0; i<geo->par->x; ++i)
        for(j=0; j<geo->par->y; ++j)
            for(k=0; k<geo->par->z; ++k) {
                if (geo->voxval[i][j][k] > 0 && geo->voxcount[i][j][k] > 0) {
                    avg = geo->voxval[i][j][k] / geo->voxcount[i][j][k];
                    if (avg < 0xFFFFFF)
                        *res = (float)avg;
                }
                ++res;
            }
}


#define ALPHA 90.0
#define S 10.0

void ccp4_header(geometry *geo) {
    ccp4header hdr;

    hdr.nc = geo->par->x;
    hdr.nr = geo->par->y;
    hdr.ns = geo->par->z;
    hdr.mode = 2;
    hdr.ncstart = 0;
    hdr.nrstart = 0;
    hdr.nsstart = 0;
    hdr.nx = geo->par->x;
    hdr.ny = geo->par->y;
    hdr.nz = geo->par->z;
    hdr.xlen = S;
    hdr.ylen = S;
    hdr.zlen = S;
    hdr.alpha = ALPHA;
    hdr.beta = ALPHA;
    hdr.gamma = ALPHA;
    hdr.mapc = 1;
    hdr.mapr = 2;
    hdr.maps = 3;
    memset(&hdr.zeros, 0, CCP4_ZEROS_HEADER_SIZE * sizeof(int32_t));
    memcpy(geo->ccp4_hdr, (char *)&hdr, sizeof(ccp4header));
}


static double ***calloc3d(size_t x, size_t y, size_t z) {
    size_t i, j;
    double ***array;

    array = (double ***)calloc(x + x * y + x * y * z, sizeof(double));
    if (!array)
        return NULL;

    for(i = 0; i < x; ++i) {
        array[i] = (double **)(array + x) + i * y;
        for(j = 0; j < y; ++j) {
            array[i][j] = (double *)(array + x + x * y) + i * y * z + j * z;
        }
    }
    return array;
}


void _destroy_ccp4(geometry *geo) {
    free(geo->mtx);
    free(geo->par);
    free(geo->lorentz);
    free(geo->voxval);
    free(geo->voxcount);
    free(geo->voxels);
    free(geo->ccp4_hdr);
    _destroy_cbf(geo->cbf);
    free(geo);
}


geometry *_init_ccp4(char *c_par, int s_par) {
    geometry *geo;

    geo = (geometry *)malloc(sizeof(geometry));
    if (!geo)
        return NULL;

    geo->mtx = (cell_matrices *)malloc(sizeof(cell_matrices));
    geo->par = (parfile *)malloc(sizeof(parfile));
    if (!geo->mtx || !geo->par)
        return NULL;

    memcpy(geo->par, c_par, s_par);
    geo->s_array = geo->par->inhor * geo->par->inver;
    geo->s_buf = geo->s_array * sizeof(double);

    geo->lorentz = (double *)malloc(geo->s_buf * 4);
    geo->voxval = calloc3d(geo->par->x, geo->par->y, geo->par->z);
    geo->voxcount = calloc3d(geo->par->x, geo->par->y, geo->par->z);
    geo->s_voxels = geo->par->x * geo->par->y * geo->par->z;
    geo->voxels = (float *)calloc(geo->s_voxels, sizeof(float));
    geo->ccp4_hdr = (char *)malloc(sizeof(ccp4header));

    if (!geo->lorentz || !geo->voxval || !geo->voxcount || !geo->ccp4_hdr)
        return NULL;

    geo->kxA = geo->lorentz + geo->s_array;
    geo->kyA = geo->kxA + geo->s_array;
    geo->kzA = geo->kyA + geo->s_array;

    geo->cbf = init_cbf_mem(_init_cbf(), geo->s_array);
    if (!geo->cbf)
        return NULL;

    return geo;
}
