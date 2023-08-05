#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "splitbbox.h"
#include "twoth.h"
#include "winshit.h"


#define D2R M_PI / 180


static inline double get_bin_number(double x0, double pos0_min, double delta) {
    return (x0 - pos0_min) / delta;
}


void bbox_integrate(integration *intg, double *image, double azmin, double azmax) {
    int i, j, bin0_max, bin0_min;
    double deltaA, deltaL, deltaR, fbin0_min, fbin0_max, max0, min0;

    memset(intg->pos->sum, 0, intg->pos->s_pos);
    memset(intg->pos->count, 0, intg->pos->s_pos);
    memset(intg->pos->merge, 0, intg->pos->s_pos);
    memset(intg->pos->sigma, 0, intg->pos->s_pos);    
    azmin *= D2R;
    azmax *= D2R;
    
    for (i=0; i<intg->pos->s_array; i++) {

        if (image[i] < 0) // intensity is unreasonable
            continue;

        if (azmin != azmax && (intg->pos->azl[i] < azmin || intg->pos->azu[i] > azmax))
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
            intg->pos->count[bin0_min] += 1;
            intg->pos->sum[bin0_min] += image[i];
        } else {
            // we have a pixel splitting
            deltaA = 1 / (fbin0_max - fbin0_min);
            deltaL = (double)bin0_min + 1 - fbin0_min;
            deltaR = fbin0_max - (double)bin0_max;
            intg->pos->count[bin0_min] += deltaA * deltaL;
            intg->pos->sum[bin0_min] += image[i] * deltaA * deltaL;
            intg->pos->count[bin0_max] += deltaA * deltaR;
            intg->pos->sum[bin0_max] += image[i] * deltaA * deltaR;

            if (bin0_min + 1 < bin0_max)
                for (j=bin0_min+1; j<bin0_max; j++) {
                    intg->pos->count[j] += deltaA;
                    intg->pos->sum[j] += image[i] * deltaA;
                }
        }
    }

    for (j=0; j<intg->pos->bins; j++)
        if (intg->pos->count[j] > 0) {
            intg->pos->merge[j] = intg->pos->sum[j] / intg->pos->count[j];
            intg->pos->sigma[j] = sqrt(intg->pos->sum[j]) / intg->pos->count[j];
        }
}
