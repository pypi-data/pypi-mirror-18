#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "splitbbox.h"


#define D2R ((float)(M_PI / 180.0))


void destroy_results(bbox_results *res) {
    if (res) {
        if (res->merge) {
            free(res->merge);
            res->merge = NULL;
            res->sigma = NULL;
        }
        free(res);
        res = NULL;
    }
}


static bbox_results *init_results(integration *intg) {
    bbox_results *res;

    res = malloc(sizeof(bbox_results));
    if (!res)
        return NULL;
    res->merge = calloc(intg->pos->bins * 2, sizeof(float));
    if (res->merge == NULL) {
        destroy_results(res);
        return NULL;
    }
    res->sigma = res->merge + intg->pos->bins;
    res->bins = intg->pos->py_bins;
    res->s_buf = res->bins * sizeof(float);
    res->shape[0] = 2;
    res->shape[1] = res->bins;
    res->strides[0] = (Py_ssize_t)res->s_buf;
    res->strides[1] = (Py_ssize_t)sizeof(float);
    return res;
}


static float get_bin_number(float x0, float pos0_min, float delta) {
    return (x0 - pos0_min) / delta;
}


bbox_results *bbox_integrate(integration *intg, float *image, float azmin, float azmax) {
    int i, j, bin0_max, bin0_min, check_azimuth;
    float deltaA, deltaL, deltaR, fbin0_min, fbin0_max, max0, min0, *count, *sum, merge, sigma;
    bbox_results *res;

    res = init_results(intg);
    if (res == NULL) {
        destroy_results(res);
        return NULL;
    }

    count = res->merge;
    sum = res->sigma;
    check_azimuth = 0;
    if (azmin != azmax) {
        check_azimuth = 1;
        if (azmin > 180)
            azmin -= 360;
        if (azmax > 180)
            azmax -= 360;
        azmin *= D2R;
        azmax *= D2R;
    }

    for (i=0; i<intg->pos->s_array; i++) {

        if (image[i] < 0) // intensity is unreasonable
            continue;

        if (check_azimuth && (intg->pos->azl[i] < azmin || intg->pos->azu[i] > azmax))
            continue;

        min0 = intg->pos->lower[i];
        max0 = intg->pos->upper[i];
        fbin0_min = get_bin_number(min0, intg->pos->min, intg->pos->delta);
        fbin0_max = get_bin_number(max0, intg->pos->min, intg->pos->delta);
        if (fbin0_max < 0 || fbin0_min >= intg->pos->bins)
            continue;
        if (fbin0_max >= intg->pos->bins)
            bin0_max = intg->pos->bins - 1;
        else
            bin0_max = (int)fbin0_max;
        if (fbin0_min < 0)
            bin0_min = 0;
        else
            bin0_min = (int)fbin0_min;

        // probably, apply corrections here
        image[i] /= intg->pos->sa[i];

        if (bin0_min == bin0_max) {
            // All pixel is within a single bin
            count[bin0_min] += 1;
            sum[bin0_min] += image[i];
        } else {
            // we have a pixel splitting
            deltaA = 1 / (fbin0_max - fbin0_min);
            deltaL = (float)bin0_min + 1 - fbin0_min;
            deltaR = fbin0_max - (float)bin0_max;
            count[bin0_min] += deltaA * deltaL;
            sum[bin0_min] += image[i] * deltaA * deltaL;
            count[bin0_max] += deltaA * deltaR;
            sum[bin0_max] += image[i] * deltaA * deltaR;
            if (bin0_min + 1 < bin0_max)
                for (j=bin0_min+1; j<bin0_max; j++) {
                    count[j] += deltaA;
                    sum[j] += image[i] * deltaA;
                }
        }
    }

    for (j=0; j<intg->pos->bins; j++)
        if (count[j] > 0) {
            merge = sum[j] / count[j];
            sigma = sqrtf(sum[j]) / count[j];
            res->merge[j] = merge;
            res->sigma[j] = sigma;
        }
    return res;
}
