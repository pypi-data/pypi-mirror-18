#ifndef CGRACIO_PONI_H_   /* Include guard */
#define CGRACIO_PONI_H_ 1


#ifndef CGRACIO_DEBUG
#define CGRACIO_DEBUG 0
#endif


typedef struct {
    double distance;
    double poni1;
    double poni2;
    double pixelsize1;
    double pixelsize2;
    double rot1;
    double rot2;
    double rot3;
    double wavelength;
    int units;
    int internal_corners;
} geometry;


typedef struct {
    int dim1;
    int dim2;
    int s_array;
    int s_buf;
    double *tth;
    double *sa;
    double *chi;
    double *dtth;
    double *dchi;
    double *upper;
    double *lower;
    double *pos;
    int bins;
    int s_pos;
    double min;
    double max;
    double delta;
    double *sum;
    double *count;
    double *merge;
    double *sigma;
    double *azl;
    double *azu;
} positions;


typedef struct {
    double  tthmax[4];
    double  chimax[4];
    double *tth[4];
    double *chi[4];
    double *deltatth[4];
    double *_deltatth[4];
    double *deltachi[4];
    double *_deltachi[4];
    double *dtth[4];
    double *dchi[4];
    double *_dchi;
    double *_dtth;
    int s_array;
    int s_buf;
} corners;


typedef struct {
    geometry *geo;
    positions *pos;
    corners *crn;
} integration;

#endif  // CGRACIO_PONI_H_
