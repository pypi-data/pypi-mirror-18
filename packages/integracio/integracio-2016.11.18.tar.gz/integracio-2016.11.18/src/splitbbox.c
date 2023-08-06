#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "splitbbox.h"
#include "twoth.h"


#define D2R M_PI / 180


static float get_bin_number(float x0, float pos0_min, float delta) {
    return (x0 - pos0_min) / delta;
}


void bbox_integrate(integration *intg, float *image, results *res) {
    int i, j, bin0_max, bin0_min;
    float deltaA, deltaL, deltaR, fbin0_min, fbin0_max, max0, min0;

    res->azmin *= D2R;
    res->azmax *= D2R;

    for (i=0; i<intg->pos->s_array; i++) {

        if (image[i] < 0) // intensity is unreasonable
            continue;

        if (res->azmin != res->azmax && (intg->pos->azl[i] < res->azmin || intg->pos->azu[i] > res->azmax))
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
            res->count[bin0_min] += 1;
            res->sum[bin0_min] += image[i];
        } else {
            // we have a pixel splitting
            deltaA = 1 / (fbin0_max - fbin0_min);
            deltaL = (float)bin0_min + 1 - fbin0_min;
            deltaR = fbin0_max - (float)bin0_max;
            res->count[bin0_min] += deltaA * deltaL;
            res->sum[bin0_min] += image[i] * deltaA * deltaL;
            res->count[bin0_max] += deltaA * deltaR;
            res->sum[bin0_max] += image[i] * deltaA * deltaR;

            if (bin0_min + 1 < bin0_max)
                for (j=bin0_min+1; j<bin0_max; j++) {
                    res->count[j] += deltaA;
                    res->sum[j] += image[i] * deltaA;
                }
        }
    }

    for (j=0; j<intg->pos->bins; j++)
        if (res->count[j] > 0) {
            res->merge[j] = res->sum[j] / res->count[j];
            res->sigma[j] = sqrt(res->sum[j]) / res->count[j];
        }
}
