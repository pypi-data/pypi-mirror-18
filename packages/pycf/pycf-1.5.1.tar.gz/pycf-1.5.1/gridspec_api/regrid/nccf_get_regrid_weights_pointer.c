/**
 * $Id: nccf_get_regrid_weights_pointer.c 915 2012-01-09 16:58:08Z pletzer $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>
#include <stdio.h>

#include <nccf_coord.h>
#include <nccf_grid.h>
#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Get the pointer to weights array, should be called after 
 * nccf_compute_regrid_weights.
 *
 * \param regrid_id object Id
 * \param datap pointer to the data
 * \return NC_NOERR on success
 *
 * \see nccf_compute_regrid_weights
 *
* \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_get_regrid_weights_pointer(int regrid_id, double **datap) {
  
  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  int totErr = NC_NOERR;
  int status;

  status = nccf_varGetDataPtr(&self->weights_stt, 
                              (void **)datap);
  totErr += abs(status);

  return totErr;
}
