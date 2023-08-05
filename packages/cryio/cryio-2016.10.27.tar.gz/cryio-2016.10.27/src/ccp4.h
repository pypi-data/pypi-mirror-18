#ifndef CRYIO_CCP4_H_   /* Include guard */
#define CRYIO_CCP4_H_ 1

#include <stdlib.h>
#include "byteoffset.h"
#include "winshit.h"


typedef struct {
    double distance;
    double wavelength;
    double alpha;
    double beta;
    double xc;
    double yc;
    double ub[3 * 3];
    double d1;
    double d2;
    double d3;
    double cell_a;
    double cell_b;
    double cell_c;
    double cell_alpha;
    double cell_beta;
    double cell_gamma;
    double b2;
    double omega0;
    double theta0;
    double kappa0;
    double phi0;
    double pixel;
    int inhor;
    int inver;
    int x;
    int y;
    int z;
    int lorentz;
    double dQ;
    int downsample;
} parfile;


typedef struct {
    double b[3][3];
    double cell[3][3];
    double ub[3][3];
    double u[3][3];
    double g[3][3];
    double uu[3][3];
} cell_matrices;


typedef struct {
    parfile *par;
    cell_matrices *mtx;
    cbfdata *cbf;
    size_t s_array;
    size_t s_buf;
    double *lorentz;
    double *kxA;
    double *kyA;
    double *kzA;
    double ***voxval;
    double ***voxcount;
    float *voxels;
    size_t s_voxels;
    char *ccp4_hdr;
} geometry;


void calc_cell_matrices(geometry *geo);

void sphere_crysalis(geometry *geo);

void cbf2ccp4(geometry *geo, double angle, double osc);

void ccp4_map(geometry *geo);


#define CCP4_ZEROS_HEADER_SIZE 237

typedef struct {          // http://www.ccp4.ac.uk/html/maplib.html#description
        int32_t nc;
        int32_t nr;
        int32_t ns;
        int32_t mode;
        int32_t ncstart;
        int32_t nrstart;
        int32_t nsstart;
        int32_t nx;
        int32_t ny;
        int32_t nz;
        float xlen;
        float ylen;
        float zlen;
        float alpha;
        float beta;
        float gamma;
        int32_t mapc;
        int32_t mapr;
        int32_t maps;
        int32_t zeros[CCP4_ZEROS_HEADER_SIZE];
} ccp4header;

void ccp4_header(geometry *geo);

void _destroy_ccp4(geometry *geo);

geometry *_init_ccp4(char *c_par, int s_par);

#endif
