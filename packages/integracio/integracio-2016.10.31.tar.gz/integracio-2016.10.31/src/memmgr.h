#ifndef CGRACIO_MEMMGR_H_   /* Include guard */
#define CGRACIO_MEMMGR_H_ 1

#include "twoth.h"

int init_positions(integration *intg, int dim1, int dim2);

integration *init_integration();

void destroy_positions(integration *intg);

void destroy_integration(integration *intg);

void destroy_corners(integration *intg);

#endif
