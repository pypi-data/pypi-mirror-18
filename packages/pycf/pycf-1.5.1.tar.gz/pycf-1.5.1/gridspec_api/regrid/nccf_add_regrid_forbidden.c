/**
 * $Id: nccf_add_regrid_forbidden.c 742 2011-05-09 19:17:59Z edhartnett $
 */

#include "nccf_regrid.h"
#include <netcdf.h>

#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Add a forbidden box, any target point inside the box will not 
 * be interpolated
 * 
 * \param regrid_id object id
 * \param lo inclusive lower set of indices delimiting the box
 * \param hi inclusive upper set of indices delimiting the box
 * \return NC_NOERR on success
 *
 * \note The order of indices in lo and hi follows C convention. 
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_add_regrid_forbidden(int regrid_id, const int lo[], const int hi[]) {

  int *lohi;
  int i;
  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);
  
  lohi = (int *) malloc(2 * self->ndims * sizeof(int));
  for (i = 0; i < self->ndims; ++i) {
    lohi[i] = lo[i];
    lohi[i + self->ndims] = hi[i];
  }
  nccf_li_add(&self->box_lohi, lohi);

  return NC_NOERR;
}
