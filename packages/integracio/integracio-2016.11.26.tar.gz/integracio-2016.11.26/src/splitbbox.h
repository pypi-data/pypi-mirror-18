#ifndef CGRACIO_SPLITBBOX_H_   /* Include guard */
#define CGRACIO_SPLITBBOX_H_ 1

#include <Python.h>
#include "twoth.h"


typedef struct {
    float *merge;
    float *sigma;
    Py_ssize_t s_buf;
    Py_ssize_t bins;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} bbox_results;


bbox_results *bbox_integrate(integration *intg, float *image, float azmin, float azmax);
void destroy_results(bbox_results *res);

#endif
