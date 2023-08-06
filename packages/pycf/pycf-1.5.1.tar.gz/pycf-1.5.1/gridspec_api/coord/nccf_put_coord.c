/**
 * Write a coordinate to file.
 *
 * $Id: nccf_put_coord.c 767 2011-06-06 23:20:19Z pletzer $
 */

#include "nccf_coord.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>

/**
 * \ingroup gs_coord_grp
 * Write object to netcdf file.
 *
 * \param coordid coordinate ID
 * \param ncid netcdf file ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_put_coord(int coordid, int ncid) {

  int status = NC_NOERR;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);

  // Write data to file
  status = nccf_writeListOfVars(ncid, 1, self->coordVar);

  return status;
}
