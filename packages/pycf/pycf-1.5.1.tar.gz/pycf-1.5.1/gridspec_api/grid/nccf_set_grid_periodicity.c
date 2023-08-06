/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_set_grid_periodicity.c 1013 2016-10-17 01:36:42Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Set the grid periodicity lengths
 *
 * \param gridid grid object Id
 * \param coord_periodicity periodicity lengths in coordinate space
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note the periodicity will typically be detected automatically so in general there 
 * is no need to call this method.
 */
int nccf_set_grid_periodicity(int gridid, 
                              const double coord_periodicity[]) {
  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);
  int i;
  for (i = 0; i < self->ndims; ++i) {
    self->coord_periodicity[i] = coord_periodicity[i];
  }
  return NC_NOERR;
}

