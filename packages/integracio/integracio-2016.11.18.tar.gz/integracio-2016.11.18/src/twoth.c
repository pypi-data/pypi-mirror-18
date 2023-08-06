#include <stdlib.h>
#include <math.h>
#include "poni.h"
#include "twoth.h"


#define HALF_PIXEL 0.5
#define DSA_ORDER 3.  // # by default we correct for 1/cos(2th), fit2d corrects for 1/cos^3(2th)
#define R2D 180 / M_PI
#define M_PI2 M_PI*M_PI
#define UNITS_TTH 0
#define UNITS_Q   1


typedef struct {
    float s1;
    float s2;
    float s3;
    float c1;
    float c2;
    float c3;
    float c2c3;
    float c3s1s2;
    float c1s3;
    float c1c3s2;
    float s1s3;
    float c2s3;
    float c1c3;
    float s1s2s3;
    float c3s1;
    float c1s2s3;
    float c2s1;
    float c1c2;
    float dt1;
    float dt2;
    float dt3;
    float c3s1s2c1s3;
    float c1c3s1s2s3;
    float pp1;
    float pp2;
    float dist2;
    float tth2q;
} geotri;


static void calc_sincos(geometry *geo, geotri *geo3) {
    geo3->c1 = cos(geo->rot1);
    geo3->c2 = cos(geo->rot2);
    geo3->c3 = cos(geo->rot3);
    geo3->s1 = sin(geo->rot1);
    geo3->s2 = sin(geo->rot2);
    geo3->s3 = sin(geo->rot3);
    geo3->c2c3 = geo3->c2 * geo3->c3;
    geo3->c3s1s2 = geo3->c3 * geo3->s1 * geo3->s2;
    geo3->c1s3 = geo3->c1 * geo3->s3;
    geo3->c1c3s2 = geo3->c1 * geo3->c3 * geo3->s2;
    geo3->s1s3 = geo3->s1 * geo3->s3;
    geo3->c2s3 = geo3->c2 * geo3->s3;
    geo3->c1c3 = geo3->c1 * geo3->c3;
    geo3->s1s2s3 = geo3->s1 * geo3->s2 * geo3->s3;
    geo3->c3s1 = geo3->c3 * geo3->s1;
    geo3->c1s2s3 = geo3->c1 * geo3->s2 * geo3->s3;
    geo3->c2s1 = geo3->c2 * geo3->s1;
    geo3->c1c2 = geo3->c1 * geo3->c2;
    geo3->dt1 = geo->distance * (geo3->c1c3s2 + geo3->s1s3);
    geo3->dt2 = geo->distance * (geo3->c3s1 - geo3->c1s2s3);
    geo3->dt3 = geo->distance * geo3->c1c2;
    geo3->c3s1s2c1s3 = geo3->c3s1s2 - geo3->c1s3;
    geo3->c1c3s1s2s3 = geo3->c1c3 + geo3->s1s2s3;
    geo3->pp1 = geo->pixelsize1 * HALF_PIXEL - geo->poni1;
    geo3->pp2 = geo->pixelsize2 * HALF_PIXEL - geo->poni2;
    geo3->dist2 = geo->distance * geo->distance;
    geo3->tth2q = 4e-9 * M_PI / geo->wavelength;
}


static void calc_part(size_t i, corners *crn) {
    *crn->deltatth[i] = fabs(*crn->dtth[i] - *crn->tth[i]);
    *crn->deltachi[i] = fmod(fabs(*crn->dchi[i] - *crn->chi[i]), M_PI2);
    crn->deltatth[i]++; crn->dtth[i]++; crn->tth[i]++;
    crn->deltachi[i]++; crn->chi[i]++; crn->chi[i]++;
}


static void calc_corners(integration *intg) {
    size_t i, j;
    float max1, max2;

    for (i=0; i<=intg->pos->dim1; ++i) {
        for (j=0; j<=intg->pos->dim2; ++j) {
            if (i == 0 || j == 0)
                intg->crn->dtth[2]++;
            else
                calc_part(2, intg->crn);
            if (i == 0 || j == intg->pos->dim2)
                intg->crn->dtth[1]++;
            else
                calc_part(1, intg->crn);
            if (i == intg->pos->dim1 || j == 0)
                intg->crn->dtth[3]++;
            else
                calc_part(3, intg->crn);
            if (i == intg->pos->dim1 || j == intg->pos->dim2)
                intg->crn->dtth[0]++;
            else
                calc_part(0, intg->crn);
        }
    }

    for (i=0; i<intg->pos->s_array; i++) {
        max1 = 0; max2 = 0;
        for (j=0; j<4; j++) {
            if (max1 < intg->crn->_deltatth[j][i])
                max1 = intg->crn->_deltatth[j][i];
            if (max2 < intg->crn->_deltachi[j][i])
                max2 = intg->crn->_deltachi[j][i];
        }
        intg->pos->dtth[i] = max1;
        intg->pos->dchi[i] = max2;
    }
}


static void bbox_positions(integration *intg) {
    int i;
    float max0, min0, delta, start, stop;

    intg->pos->min = 0;
    intg->pos->max = 0;

    for (i=0; i<intg->pos->s_array; i++) {
        min0 = intg->pos->tth[i] - intg->pos->dtth[i];
        max0 = intg->pos->tth[i] + intg->pos->dtth[i];
        intg->pos->upper[i] = max0;
        intg->pos->lower[i] = min0;
        if (max0 > intg->pos->max)
            intg->pos->max = max0;
        if (min0 < intg->pos->min)
            intg->pos->min = min0;
        intg->pos->azl[i] = intg->pos->chi[i] + intg->pos->dchi[i];
        intg->pos->azu[i] = intg->pos->chi[i] - intg->pos->dchi[i];
    }

    if (intg->pos->min < 0)
        intg->pos->min = 0;

    intg->pos->delta = (intg->pos->max - intg->pos->min) / intg->pos->bins;
    start = intg->pos->min + HALF_PIXEL * intg->pos->delta;
    stop  = intg->pos->max - HALF_PIXEL * intg->pos->delta;
    delta = (stop - start) / (intg->pos->bins - 1);
    for (i=0; i<intg->pos->bins; i++) {
        intg->pos->pos[i] = start + delta * i;
        if (intg->geo->units == UNITS_TTH)
            intg->pos->pos[i] *= R2D;
    }
}


void calculate_positions(integration *intg) {
    int i, j;
    float p1, p2, t1, t2, t3, t11, t21, t31, dp1, dp2, _dtth, _tth, *dtth, *dchi;
    float dt11, dt21, dt31, dt1, dt2, dt3, p1i, p2j, p11, *tth, *sa, *chi;
    geotri geo3;

    tth = intg->pos->tth;
    sa = intg->pos->sa;
    chi = intg->pos->chi;
    dtth = intg->crn->_dtth;
    dchi = intg->crn->_dchi;
    t11 = 0; t21 = 0; t31 = 0;
    calc_sincos(intg->geo, &geo3);
    for (i=0; i<=intg->pos->dim1; i++) {
        p1i = intg->geo->pixelsize1 * i;
        p1 = p1i + geo3.pp1;
        p11 = geo3.dist2 + p1 * p1;
        dp1 = p1i - intg->geo->poni1;
        t11 = p1 * geo3.c2c3 - geo3.dt1;
        dt11 = dp1 * geo3.c2c3 - geo3.dt1;
        t21 = p1 * geo3.c2s3 + geo3.dt2;
        dt21 = dp1 * geo3.c2s3 + geo3.dt2;
        t31 = p1 * geo3.s2 + geo3.dt3;
        dt31 = dp1 * geo3.s2 + geo3.dt3;
        for (j=0; j<=intg->pos->dim2; j++) {
            p2j = intg->geo->pixelsize2 * j;
            p2 = p2j + geo3.pp2;
            dp2 = p2j - intg->geo->poni2;
            t1 = t11 + p2 * geo3.c3s1s2c1s3;
            dt1 = dt11 + dp2 * geo3.c3s1s2c1s3;
            t2 = t21 + p2 * geo3.c1c3s1s2s3;
            dt2 = dt21 + dp2 * geo3.c1c3s1s2s3;
            t3 = t31 - p2 * geo3.c2s1;
            dt3 = dt31 - dp2 * geo3.c2s1;
            _dtth = atan2(sqrt(dt1 * dt1 + dt2 * dt2), dt3);
            if (intg->geo->units == UNITS_Q)
                _dtth = geo3.tth2q * sin(_dtth / 2);
            *dtth++ = _dtth;
            *dchi++ = atan2(dt1, dt2);
            if (i != intg->pos->dim1 && j != intg->pos->dim2) {
                _tth = atan2(sqrt(t1 * t1 + t2 * t2), t3);
                if (intg->geo->units == UNITS_Q)
                    _tth = geo3.tth2q * sin(_tth / 2);
                *tth++ = _tth;
                *sa++ = pow(intg->geo->distance / sqrt(p11 + p2 * p2), DSA_ORDER);
                *chi++ = atan2(t1, t2);
            }
        }
    }
    calc_corners(intg);
    bbox_positions(intg);
}
