/*
 * $Id: nccf_inq_axis_datatype.c 772 2011-06-13 15:00:28Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_axis_grp
 * Inquire the axis data type.
 *
 * \param axisid axis ID
 * \param xtype data type
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_axis_datatype(int axisid, nc_type *xtype) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);

  *xtype = self->xtype;

  return status;
}
