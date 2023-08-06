#ifndef CGRACIO_PONI_H_   /* Include guard */
#define CGRACIO_PONI_H_ 1

#include <stdint.h>

#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif        // M_PI


typedef struct {
    float distance;
    float poni1;
    float poni2;
    float pixelsize1;
    float pixelsize2;
    float rot1;
    float rot2;
    float rot3;
    float wavelength;
    int units;
} geometry;


typedef struct {
    int dim1;
    int dim2;
    int s_array;
    int s_buf;
    float *tth;
    float *sa;
    float *chi;
    float *dtth;
    float *dchi;
    float *upper;
    float *lower;
    float *pos;
    int bins;
    int s_pos;
    float min;
    float max;
    float delta;
    float *azl;
    float *azu;
} positions;


typedef struct {
    float *count;
    float *merge;
    float *sigma;
    float *sum;
    float azmin;
    float azmax;
} results;


typedef struct {
    float *tth[4];
    float *chi[4];
    float *deltatth[4];
    float *_deltatth[4];
    float *deltachi[4];
    float *_deltachi[4];
    float *dtth[4];
    float *dchi[4];
    float *_dchi;
    float *_dtth;
    int s_array;
    int s_buf;
} corners;


typedef struct {
    geometry *geo;
    positions *pos;
    corners *crn;
} integration;

#endif  // CGRACIO_PONI_H_
