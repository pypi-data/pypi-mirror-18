#include <stdlib.h>
#include <string.h>
#include "poni.h"
#include "twoth.h"
#include "memmgr.h"


int init_aux(integration *intg) {
    char *mem;
    float *m;
    size_t i;

    intg->crn->s_array = (intg->pos->dim1 + 1) * (intg->pos->dim2 + 1);
    intg->crn->s_buf = intg->crn->s_array * sizeof(float);

    mem = malloc(intg->crn->s_buf * 2 + intg->pos->s_buf * 4 * 3 + intg->pos->s_pos);
    if (!mem)
        return 0;

    intg->pos->tth = (float *)mem;
    intg->pos->chi = intg->pos->tth + intg->pos->s_array;
    intg->pos->dchi = intg->pos->chi + intg->pos->s_array;
    intg->pos->dtth = intg->pos->dchi + intg->pos->s_array;
    intg->pos->pos = intg->pos->dtth + intg->pos->s_array;
    intg->crn->_dtth = intg->pos->pos + intg->pos->bins;
    intg->crn->_dchi = intg->crn->_dtth + intg->crn->s_array;

    m = intg->crn->_dtth + intg->crn->s_array * 2;
    for (i=0; i<4; ++i) {
        intg->crn->tth[i]       = intg->pos->tth;
        intg->crn->chi[i]       = intg->pos->chi;
        intg->crn->dtth[i]      = intg->crn->_dtth;
        intg->crn->dchi[i]      = intg->crn->_dchi;
        intg->crn->deltatth[i]  = m + intg->pos->s_array * i;
        intg->crn->deltachi[i]  = m + intg->pos->s_array * 4 + intg->pos->s_array * i;
        intg->crn->_deltatth[i] = intg->crn->deltatth[i];
        intg->crn->_deltachi[i] = intg->crn->deltachi[i];
    }
    return 1;
}


int init_positions(integration *intg, int dim1, int dim2) {
    char *mem;

    intg->pos->dim1 = dim1;
    intg->pos->dim2 = dim2;
    intg->pos->s_array = intg->pos->dim1 * intg->pos->dim2;
    intg->pos->s_buf = sizeof(float) * intg->pos->s_array;
    intg->pos->bins = (intg->pos->dim1 >= intg->pos->dim2) ? intg->pos->dim1 * 2 : intg->pos->dim2 * 2;
    intg->pos->s_pos = sizeof(float) * intg->pos->bins;

    mem = malloc(intg->pos->s_buf * 5);
    if (!mem)
        return 0;

    intg->pos->lower = (float *)mem;
    intg->pos->upper = intg->pos->lower + intg->pos->s_array;
    intg->pos->azl = intg->pos->upper + intg->pos->s_array;
    intg->pos->azu = intg->pos->azl + intg->pos->s_array;
    intg->pos->sa = intg->pos->azu + intg->pos->s_array;
    return 1;
}


void destroy_aux(integration *i) {
    if (i) {
        if (i->pos->tth) {
            free(i->pos->tth);
            i->pos->pos = NULL;
            i->pos->tth = NULL;
            i->pos->chi = NULL;
            i->pos->dchi = NULL;
            i->pos->dtth = NULL;
            i->crn->_dtth = NULL;
            i->crn->_dchi = NULL;
        }
    }
}


void destroy_integration(integration *i) {
    destroy_aux(i);
    if (i) {
        if (i->pos->lower) {
            free(i->pos->lower);
            i->pos->lower = NULL;
            i->pos->upper = NULL;
            i->pos->azl = NULL;
            i->pos->azu = NULL;
            i->pos->sa = NULL;
        }
        free(i);
        i = NULL;
    }
}


integration *init_integration() {
    char *mem;
    integration *i;

    mem = malloc(
        sizeof(integration) +
        sizeof(geometry)    +
        sizeof(positions)   +
        sizeof(corners)
    );
    if (!mem)
        return NULL;

    i = (integration *)mem;
    i->geo = (geometry *)(i + 1);
    i->pos = (positions *)(i->geo + 1);
    i->crn = (corners *)(i->pos + 1);

    i->pos->tth   = NULL;
    i->pos->sa    = NULL;
    i->pos->chi   = NULL;
    i->pos->dchi  = NULL;
    i->pos->dtth  = NULL;
    i->pos->upper = NULL;
    i->pos->lower = NULL;
    i->pos->pos   = NULL;
    i->pos->azl   = NULL;
    i->pos->azu   = NULL;
    i->crn->_dtth = NULL;
    i->crn->_dchi = NULL;
    i->pos->dim1  = 0;
    i->pos->dim2  = 0;
    i->crn->s_array = 0;
    i->crn->s_buf   = 0;

    return i;
}


results *init_results(integration *intg) {
    results *res;

    res = (results *)malloc(sizeof(results));
    if (!res)
        return NULL;
    res->count = calloc(intg->pos->bins * 4, sizeof(float));
    if (!res->count) {
        destroy_results(res);
        return NULL;
    }
    res->merge = res->count + intg->pos->bins;
    res->sigma = res->merge + intg->pos->bins;
    res->sum = res->sigma + intg->pos->bins;
    return res;
}


void destroy_results(results *res) {
    if (res) {
        if (res->count) {
            free(res->count);
            res->count = NULL;
        }
        free(res);
        res = NULL;
    }
}
