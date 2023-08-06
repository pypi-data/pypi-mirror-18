/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_inq_grid_periodicity.c 894 2011-12-21 22:21:14Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Get the grid periodicity lengths
 *
 * \param gridid grid object Id
 * \param coord_periodicity (output) periodicity lengths in coordinate space
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note very large numbers are returned for non-periodic indices/coordinates
 */
int nccf_inq_grid_periodicity(int gridid, 
                              double coord_periodicity[]) {
  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);
  int i;
  for (i = 0; i < self->ndims; ++i) {
    coord_periodicity[i] = self->coord_periodicity[i];
  }
  return NC_NOERR;
}

