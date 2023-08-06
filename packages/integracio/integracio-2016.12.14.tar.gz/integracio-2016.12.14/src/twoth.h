#ifndef CGRACIO_TWOTHETA_H_   /* Include guard */
#define CGRACIO_TWOTHETA_H_ 1

#include <stdint.h>
#include <Python.h>

#ifndef M_PI
    #define M_PI 3.14159265358979323846f
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
    float radmin;
    float radmax;
} geometry;


typedef struct {
    int dim1;
    int dim2;
    int s_array;
    int s_buf;
    float *tth;
    float *sa;
    float *chi;
    float *upper;
    float *lower;
    float *pos;
    int bins;
    Py_ssize_t py_bins;
    int s_pos;
    float min;
    float max;
    float delta;
    float *azl;
    float *azu;
} positions;


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
    positions *pos;
    corners *crn;
} integration;


integration *calculate_positions(int dim1, int dim2, geometry *geo);
void destroy_integration(integration *intg);

#endif
