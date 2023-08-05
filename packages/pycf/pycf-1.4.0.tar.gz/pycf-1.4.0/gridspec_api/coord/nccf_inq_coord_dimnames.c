/**
 * $Id: nccf_inq_coord_dimnames.c 895 2011-12-22 13:12:38Z pletzer $
 */

#include "cf_config.h"
#include <nccf_varObj.h>
#include <nccf_coord.h>
#include <string.h>

/**
 * \ingroup gs_coord_grp
 * Fill in the dimension names.
 *
 * \param coordid coordinate ID
 * \param dimnames (output) array of dimension names for each axis
 * \return NC_NOERR on success
 */
int nccf_inq_coord_dimnames(int coordid, char **dimnames) {
  int i, status, ndims;
  struct nccf_coord_type *self;
  const char *dimName;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  status = nccf_varGetNumDims(&self->coordVar, &ndims);
  for (i = 0; i < ndims; ++i) {
    nccf_varGetDimNamePtr(&self->coordVar, i, &dimName);
    strncpy(dimnames[i], dimName, STRING_SIZE);
  }
  return status;
}
