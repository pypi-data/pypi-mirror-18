#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "poni.h"
#include "twoth.h"
#include "winshit.h"


#define HALF_PIXEL 0.5
#define DSA_ORDER 3.  // # by default we correct for 1/cos(2th), fit2d corrects for 1/cos^3(2th)
#define R2D 180 / M_PI
#define M_PI2 M_PI*M_PI
#define UNITS_TTH 0
#define UNITS_Q   1


typedef struct {
    double s1;
    double s2;
    double s3;
    double c1;
    double c2;
    double c3;
    double c2c3;
    double c3s1s2;
    double c1s3;
    double c1c3s2;
    double s1s3;
    double c2s3;
    double c1c3;
    double s1s2s3;
    double c3s1;
    double c1s2s3;
    double c2s1;
    double c1c2;
    double dt1;
    double dt2;
    double dt3;
    double c3s1s2c1s3;
    double c1c3s1s2s3;
    double pp1;
    double pp2;
    double dist2;
    double tth2q;
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
    if (crn->tthmax[i] < *crn->deltatth[i])
       crn->tthmax[i] = *crn->deltatth[i];
    *crn->deltachi[i] = fmod(fabs(*crn->dchi[i] - *crn->chi[i]), M_PI2);
    if (crn->chimax[i] < *crn->deltachi[i])
       crn->chimax[i] = *crn->deltachi[i];
    crn->deltatth[i]++; crn->dtth[i]++; crn->tth[i]++;
    crn->deltachi[i]++; crn->chi[i]++; crn->chi[i]++;
}


static void calc_corners(integration *intg) {
    size_t i, j, k;
    double max1, max2;

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

    j = 0; max1 = intg->crn->tthmax[0];
    k = 0; max2 = intg->crn->chimax[0];
    for (i=0; i<4; ++i) {
        if (max1 < intg->crn->tthmax[i]) {
            j = i;
            max1 = intg->crn->tthmax[i];
        }
        if (max2 < intg->crn->chimax[i]) {
            k = i;
            max2 = intg->crn->chimax[i];
        }
    }

    memcpy(intg->pos->dtth, intg->crn->_deltatth[j], intg->pos->s_buf);
    memcpy(intg->pos->dchi, intg->crn->_deltachi[k], intg->pos->s_buf);
}


void bbox_positions(integration *intg) {
    int i;
    double max0, min0, delta, start, stop;

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
    double p1, p2, t1, t2, t3, t11, t21, t31, dp1, dp2, _dtth, _tth, *dtth, *dchi;
    double dt11, dt21, dt31, dt1, dt2, dt3, p1i, p2j, p11, *tth, *sa, *chi;
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
    if (intg->geo->internal_corners) {
        calc_corners(intg);
        bbox_positions(intg);
    }
}
