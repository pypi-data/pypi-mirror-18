/*
 * API to write a structured grid to a file
 *
 * $Id: nccf_put_grid.c 966 2016-09-07 01:26:41Z pletzer $
 */

#include <nccf_grid.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>
#include <libcf_src.h>
#include <nccf_errors.h>
#include <nccf_coord.h>

/**
 * \ingroup gs_grid_grp
 * Write structured grid, including its underlying coordinates.
 *
 * \param gridid grid ID
 * \param ncid NetCDF file ID created by nc_create or nc_open
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_put_grid(int gridid, int ncid) {

  int status, ndims, iDim;
  int totErr = 0;
  int catchErr = NC_NOERR;

// Open the grid structure.
  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

// Get the coordinate IDs
  int coordids[self->ndims];
  status = nccf_inq_grid_coordids(gridid, coordids);
  totErr += abs(status);

// Get the dimensions and the coordinate IDs.
  status = nccf_inq_coord_ndims(coordids[0], &ndims);
  totErr += abs(status);

// Write coordinate data to file
  for(iDim = 0; iDim < ndims; iDim++) {
    status = nccf_put_coord(coordids[iDim], ncid);
    totErr += abs(status);
  }

// Write mask, if present
  if (self->imask && self->ndims > 0) {
    struct nccf_var_obj *imask_var;
    status = nccf_varCreate(&imask_var, "imask");
    int dims[self->ndims];
    char **dimnames;
    dimnames = (char **) malloc(sizeof(char *) * self->ndims);
    for (iDim = 0; iDim < ndims; ++iDim) {
      dimnames[iDim] = (char *) calloc(STRING_SIZE, sizeof(char));
    }
    status = nccf_inq_coord_dims(coordids[0], dims);
    status = nccf_inq_coord_dimnames(coordids[0], dimnames);
    status = nccf_varSetDims(&imask_var, self->ndims, dims, 
			     (const char **) dimnames);
    status = nccf_varSetAttribText(&imask_var, "units", "unitless");
    status = nccf_varSetAttribText(&imask_var, "long_name", 
			     "array mask (0=invalid, 1=valid)");
    status = nccf_varSetDataPtr(&imask_var, NC_INT, self->imask);
    status = nccf_writeListOfVars(ncid, 1, imask_var);
    status = nccf_varDestroy(&imask_var);
    for (iDim = 0; iDim < ndims; ++iDim) {
      free(dimnames[iDim]);
    }
    free(dimnames);
  }

  if (totErr != 0) {
    if (catchErr != NC_NOERR) {
      return catchErr;
    }
    else {
      return NCCF_EPUTGRID;
    }
  }
  return NC_NOERR;
}
