/**
 * $Id: nccf_free_regrid.c 918 2012-02-07 22:10:36Z pletzer $
 */

#include "nccf_regrid.h"
#include <netcdf.h>

#include <nccf_utility_functions.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_regrid_grp
 * Free regridding object (destructor).
 *
 * \param regrid_id object Id.
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_free_regrid(int regrid_id) {

  int *lohi;
  int id;
  struct nccf_regrid_type *self;
  self = nccf_li_remove(&CFLIST_REGRID, regrid_id);
  if( nccf_li_get_nelem( &CFLIST_REGRID ) == 0 )
      nccf_li_del( &CFLIST_REGRID );

  /* Clean up */
  nccf_li_begin(&self->box_lohi);
  while (nccf_li_next(&self->box_lohi)) {
    id = nccf_li_get_id(&self->box_lohi);
    lohi = nccf_li_remove(&self->box_lohi, id);
    free(lohi);
    lohi = NULL;
  }
  nccf_li_del(&self->box_lohi);
  
  nccf_varDestroy(&self->weights_stt);
  nccf_varDestroy(&self->lower_corner_indices_stt);
  nccf_varDestroy(&self->inside_domain_stt);

  free(self);
  self = NULL;

  return NC_NOERR;
}
