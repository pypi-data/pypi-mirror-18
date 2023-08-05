/**
 * Get the number of space dimensions
 *
 * $Id: nccf_inq_coord_ndims.c 895 2011-12-22 13:12:38Z pletzer $
 */

#include "nccf_coord.h"

/**
 * \ingroup gs_coord_grp
 * Get the the number of dimensions.
 *
 * \param coordid coordinate ID
 * \param ndims (output) number of space dims
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_coord_ndims(int coordid, int *ndims) {
  int status;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  status = nccf_varGetNumDims(&self->coordVar, ndims);
  return status;
}
