#ifndef CGRACIO_MEMMGR_H_   /* Include guard */
#define CGRACIO_MEMMGR_H_ 1

#include "twoth.h"

integration *init_integration();
int init_positions(integration *intg, int dim1, int dim2);
int init_aux(integration *intg);
void destroy_aux(integration *i);
results *init_results(integration *intg);
void destroy_results(results *res);
void destroy_integration(integration *i);
#endif
