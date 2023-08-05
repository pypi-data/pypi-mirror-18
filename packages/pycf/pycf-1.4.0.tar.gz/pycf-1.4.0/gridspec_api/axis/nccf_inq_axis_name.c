/*
 * $Id: nccf_inq_axis_name.c 772 2011-06-13 15:00:28Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_axis_grp
 * Inquire the name of the axis.
 *
 * \param axisid axis ID
 * \param name name of object, also dimension name
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 * \note container name should be large enough the receive the 
 *       name of the axis
 */
int nccf_inq_axis_name(int axisid, char *name) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);

  strcpy(name, self->axis_name);

  return status;
}
