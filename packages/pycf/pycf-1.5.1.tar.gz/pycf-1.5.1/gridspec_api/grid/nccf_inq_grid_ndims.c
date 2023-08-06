/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_inq_grid_ndims.c 822 2011-09-13 14:39:33Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Get number of space dimensions.
 *
 * \param gridid grid object Id
 * \param ndims (output) number of space dimensions
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_grid_ndims(const int gridid, int *ndims ){

   struct nccf_struct_grid_type *self;
   self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);
   *ndims = self->ndims;

   return NC_NOERR;
}
