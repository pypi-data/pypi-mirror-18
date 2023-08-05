/**
 * Get the space dimensions
 *
 * $Id: nccf_inq_coord_dims.c 895 2011-12-22 13:12:38Z pletzer $
 */

#include "nccf_coord.h"

/**
 * \ingroup gs_coord_grp
 * Fill in the dimensions.
 *
 * \param coordid coordinate ID
 * \param dims (output) array of dimensions for each axis
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_coord_dims(int coordid, int *dims) {
  int i, status, ndims;
  int *dimsPtr;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  status = nccf_varGetNumDims(&self->coordVar, &ndims);
  status = nccf_varGetDimsPtr(&self->coordVar, &dimsPtr);
  for (i = 0; i < ndims; ++i) {
    dims[i] = dimsPtr[i];
  }
  return status;
}
