/*
 * $Id: nccf_put_axis.c 767 2011-06-06 23:20:19Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>

/**
 * \ingroup gs_axis_grp
 * Write object to netcdf file.
 *
 * \param axisid axis ID
 * \param ncid netcdf file ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int nccf_put_axis(int axisid, int ncid) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);

  // Write data to file
  status = nccf_writeListOfVars(ncid, 1, self->axisVar);

  return status;
}
