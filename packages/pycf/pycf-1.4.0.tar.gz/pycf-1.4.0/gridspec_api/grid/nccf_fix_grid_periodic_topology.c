/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_fix_grid_periodic_topology.c 1013 2016-10-17 01:36:42Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Fix the grid periodic topology
 *
 * \param gridid grid object Id
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, NeSI/NIWA.
 * \note for cases where the grid coordinates wrap around, this 
 *       method will add/subtract a periodicity length to produce
 *       the smallest cells. 
 */
int nccf_fix_grid_periodic_topology(int gridid) {

  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

  int i, j, coordids[self->ndims], dims[self->ndims]; 
  int indices[self->ndims];
  int status;
  int totError = NC_NOERR;
  double* coords = NULL;
  double hmin, h;
  int ntot, k, kPlus, jmin;

  status = nccf_inq_grid_coordids(gridid, coordids);
  totError += abs(status);

  if (self->ndims <= 0) {
    /* nothing to do, must have at least one dimension */
    return NC_NOERR;
  }

  /* determine the number of nodes */
  status = nccf_inq_coord_dims(coordids[0], dims);
  totError += abs(status);
  ntot = 1;
  for (i = 0; i < self->ndims; ++i) {
    ntot *= dims[i];
  }

  /* iterate over the periodic topological dimensions */
  for (i = 0; i < self->ndims; ++i) {

    status = nccf_get_coord_data_pointer(coordids[i], &coords);
    totError += abs(status);

    /* only consider periodic directions */
    if (self->coord_periodicity[i] < CF_HUGE_DOUBLE) {

      /* iterate over the nodes */
      for (k = 0; k < ntot; ++k) {

        /* get the index set */
        status = nccf_get_multi_index(self->ndims, dims, k, indices);
        totError += abs(status);

        if (indices[i] >= dims[i] - 1) {
          /* high side, cannot comute the cell size */
          continue;
        }


        indices[i]++;
        kPlus = nccf_get_flat_index(self->ndims, dims, indices);

        /*add/subtract a periodicity length if this reduces the cell size */
        jmin = 2;
        hmin = CF_HUGE_DOUBLE;
        for (j = -1; j < 2; ++j) {
          h = coords[kPlus] + j*self->coord_periodicity[i] - coords[k];
          if (fabs(h) < hmin) {
            hmin = fabs(h);
            jmin = j;
          }
        }

        coords[kPlus] += jmin*self->coord_periodicity[i];
      } /* end of node itereation */

    } /* end of periodic test */

  }

  return totError;
}

