/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_inq_grid_coordids.c 1002 2016-10-04 02:39:44Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Fill in coordinate ids stored in a grid object.
 *
 * \param gridid grid object Id
 * \param coordids (output) list of coordinate ids
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_grid_coordids(const int gridid, int coordids[]) {

   int i;
   struct nccf_struct_grid_type *self;

   self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

   for (i = 0; i < self->ndims; ++i) {
     coordids[i] = self->coordids[i];
   }

   return NC_NOERR;
}
