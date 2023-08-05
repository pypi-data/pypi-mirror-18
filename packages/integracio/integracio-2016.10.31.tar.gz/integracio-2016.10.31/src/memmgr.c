#include <stdlib.h>
#include <string.h>
#include "poni.h"
#include "twoth.h"
#include "memmgr.h"


static void null_positions(integration *intg) {
    if (intg && intg->pos) {
        intg->pos->tth   = NULL;
        intg->pos->sa    = NULL;
        intg->pos->chi   = NULL;
        intg->pos->dchi  = NULL;
        intg->pos->dtth  = NULL;
        intg->pos->upper = NULL;
        intg->pos->lower = NULL;
        intg->pos->pos   = NULL;
        intg->pos->sum   = NULL;
        intg->pos->count = NULL;
        intg->pos->merge = NULL;
        intg->pos->sigma = NULL;
        intg->pos->azl   = NULL;
        intg->pos->azu   = NULL;
        intg->pos->dim1  = 0;
        intg->pos->dim2  = 0;
    }
}


static void null_corners(integration *intg) {
    if (intg && intg->crn) {
        intg->crn->_dtth   = NULL;
        intg->crn->_dchi   = NULL;
        intg->crn->s_array = 0;
        intg->crn->s_buf   = 0;
    }
}


static int init_corners(integration *intg) {
    double *mem;
    size_t i;

    intg->crn->s_array = (intg->pos->dim1 + 1) * (intg->pos->dim2 + 1);
    intg->crn->s_buf = intg->crn->s_array * sizeof(double);
    i = intg->crn->s_buf * 2;
    if (intg->geo->internal_corners)
        i += intg->pos->s_buf * 4 * 2;
    mem = (double *)malloc(i);
    if (!mem)
        return 0;
    intg->crn->_dtth = mem;
    intg->crn->_dchi = mem + intg->crn->s_array;
    if (intg->geo->internal_corners) {
        mem += intg->crn->s_array * 2;
        for (i=0; i<4; ++i) {
            intg->crn->tthmax[i]    = 0;
            intg->crn->chimax[i]    = 0;
            intg->crn->tth[i]       = intg->pos->tth;
            intg->crn->chi[i]       = intg->pos->chi;
            intg->crn->dtth[i]      = intg->crn->_dtth;
            intg->crn->dchi[i]      = intg->crn->_dchi;
            intg->crn->deltatth[i]  = mem + intg->pos->s_array * i;
            intg->crn->deltachi[i]  = mem + intg->pos->s_array * 4 + intg->pos->s_array * i;
            intg->crn->_deltatth[i] = intg->crn->deltatth[i];
            intg->crn->_deltachi[i] = intg->crn->deltachi[i];
        }
    }
    return 1;
}


int init_positions(integration *intg, int dim1, int dim2) {
    double *mem;

    if (intg->pos->dim1 == dim1 && intg->pos->dim2 == dim2)
        return 1;

    destroy_positions(intg);
    destroy_corners(intg);

    intg->pos->dim1 = dim1;
    intg->pos->dim2 = dim2;
    intg->pos->s_array = intg->pos->dim1 * intg->pos->dim2;
    intg->pos->s_buf = sizeof(double) * intg->pos->s_array;
    intg->pos->bins = (intg->pos->dim1 >= intg->pos->dim2) ? intg->pos->dim1 * 2 : intg->pos->dim2 * 2;
    intg->pos->s_pos = sizeof(double) * intg->pos->bins;

    if (!(mem = (double *)malloc(intg->pos->s_buf * 9 + intg->pos->s_pos * 5)))
        return 0;

    intg->pos->tth   = mem;
    intg->pos->sa    = intg->pos->tth + intg->pos->s_array;
    intg->pos->chi   = intg->pos->sa + intg->pos->s_array;
    intg->pos->dchi  = intg->pos->chi + intg->pos->s_array;
    intg->pos->dtth  = intg->pos->dchi + intg->pos->s_array;
    intg->pos->upper = intg->pos->dtth + intg->pos->s_array;
    intg->pos->lower = intg->pos->upper + intg->pos->s_array;
    intg->pos->azl   = intg->pos->lower + intg->pos->s_array;
    intg->pos->azu   = intg->pos->azl + intg->pos->s_array;
    intg->pos->pos   = intg->pos->azu + intg->pos->s_array;
    intg->pos->sum   = intg->pos->pos + intg->pos->bins;
    intg->pos->count = intg->pos->sum + intg->pos->bins;
    intg->pos->merge = intg->pos->count + intg->pos->bins;
    intg->pos->sigma = intg->pos->merge + intg->pos->bins;
    return init_corners(intg);

}


void destroy_positions(integration *intg) {
    if (intg && intg->pos && intg->pos->tth) {
        free(intg->pos->tth);
        null_positions(intg);
    }
}


void destroy_corners(integration *intg) {
    if (intg && intg->crn && intg->crn->_dtth) {
        free(intg->crn->_dtth);
        null_corners(intg);
    }
}


void destroy_integration(integration *intg) {
    if (intg) {
        destroy_corners(intg);
        destroy_positions(intg);
        free(intg->pos);
        free(intg->geo);
        free(intg->crn);
        free(intg);
    }
}


integration *init_integration() {
    integration *intg;

    if (!(intg = (integration *)malloc(sizeof(integration))))
        return NULL;
    if (!(intg->geo = (geometry *)malloc(sizeof(geometry))))
        return NULL;
    if (!(intg->pos = (positions *)malloc(sizeof(positions))))
        return NULL;
    if (!(intg->crn = (corners *)malloc(sizeof(corners))))
        return NULL;
    null_positions(intg);
    null_corners(intg);
    return intg;
}
