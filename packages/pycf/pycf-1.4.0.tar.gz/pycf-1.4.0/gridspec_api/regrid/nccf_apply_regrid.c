/**
 * $Id: nccf_apply_regrid.c 787 2011-07-28 19:04:22Z dkindig $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>
#include <stdio.h>

#include <nccf_data.h>
#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Regrid data, should be called after nccf_compute_regrid_weights.
 *
 * \param regrid_id object Id
 * \param ori_data_id data object on original grid
 * \param tgt_data_id data object on target grid
 * \return NC_NOERR on success
 *
 * \see nccf_compute_regrid_weights
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_apply_regrid(int regrid_id, int ori_data_id, int tgt_data_id) {
  
  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  int totErr = NC_NOERR;
  int status;

  nc_type dType;
  status =  nccf_inq_data_type(tgt_data_id, &dType);
  totErr += abs(status);

  int i, j;
  int nNodes = 1;
  for (i = 0; i < self->ndims; ++i) {
    nNodes *= 2;
  }

  if (dType == NC_DOUBLE) {
#define _TYPE double
#include "nccf_apply_regrid_type.h"
#undef _TYPE
  }
  else if (dType == NC_FLOAT) {
#define _TYPE float
#include "nccf_apply_regrid_type.h"
#undef _TYPE
  }
  else {
    /* not supported */
    totErr += 1;
  }

  return totErr;
}
