/**
 * $Id: nccf_def_grid_from_file.c 977 2016-09-12 04:56:44Z pletzer $
 */

#include <nccf_constants.h>
#include "nccf_grid.h"
#include <netcdf.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

#include "nccf_varObj.h"
#include "nccf_coord.h"
#include "nccf_global.h"
#include "nccf_errors.h"

/**
 * \ingroup gs_grid_grp
 * Define (construct) grid from a netcdf file.
 *
 * \param filename name of the netcdf file
 * \param ndims number of space dimensions
 * \param coordnames name of each coordinate (each string should be able to hold at least NC_MAX_NAME characters)
 * \param gridid (output) returned grid ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 * \note This will recusively call the define method for the coordinates.
 */
int nccf_def_grid_from_file(const char *filename,
                   int ndims,
                   const char **coordnames,
                   int *gridid) {

  printf("*** in nccf_def_grid_from_file\n");
  int totError = NC_NOERR, status = NC_NOERR, globalid;
  int ncid, i;

  /* Create the structure */
  struct nccf_struct_grid_type *self;
  self = (struct nccf_struct_grid_type *)
          malloc(sizeof( struct nccf_struct_grid_type));

  /* Initialize */
  self->ndims = ndims;
  self->coordids = (int *) malloc(ndims * sizeof(int));
  self->gridname = NULL;
  self->imask = NULL;
  self->coord_periodicity = NULL;

  /* Open file */
  status = nc_open(filename, NC_NOWRITE, &ncid);
  if (status) return status;
  totError += abs(status);

  /* Read in the coordinates */
  for (i = 0; i < ndims; ++i) {
    printf("*** i = %d coordname = %s\n", i, coordnames[i]);
    status = nccf_def_coord_from_file(filename, coordnames[i], 
                                      &self->coordids[i]);
    totError += abs(status);
  }

  /* Read in the mask, if present */
  int var_id;
  if (ndims > 0 && nc_inq_varid(ncid, "imask", &var_id) == NC_NOERR) {
    // compute number of vertices
    int dims[ndims];
    status = nccf_inq_coord_dims(self->coordids[0], dims);
    totError += abs(status);
    int nvertex = 1;
    for (i = 0; i < ndims; ++i) {
      nvertex *= dims[i];
    }
    // read the netcdf variable "imask"
    const int read_data = 1;
    const int keep_type = 0;
    struct nccf_var_obj *imask_var;
    status = nccf_varCreateFromFile(&imask_var, "imask", ncid, 
                                    read_data, keep_type);
    totError += abs(status);
    // get the pointer
    int *imask;
    status = nccf_varGetDataPtr(&imask_var, (void **) &imask);
    totError += abs(status);
    // set the mask values
    self->imask = (int *) malloc(nvertex * sizeof(int));
    for (i = 0; i < nvertex; ++i) {
      self->imask[i] = imask[i];
    }
    // clean up
    status = nccf_varDestroy(&imask_var);
  }
  
  /* Fill in the gridname */
  self->gridname = (char*) malloc(STRING_SIZE * sizeof(char));
  status = nccf_def_global_from_file( filename, &globalid );
  status = nccf_inq_global_att( globalid, CF_GRIDNAME, self->gridname );
  nccf_free_global( globalid );

  /* Close the file */
  status = nc_close( ncid );
  totError += abs(status);

  /* Get the ID */
  if (CFLIST_STRUCTURED_GRID == NULL) nccf_li_new(&CFLIST_STRUCTURED_GRID);
  *gridid = nccf_li_add( &CFLIST_STRUCTURED_GRID, self );

  status = nccf_detect_grid_periodicity(self);
  totError += abs(status);

  return totError;
}
