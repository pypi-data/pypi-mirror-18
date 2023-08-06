/*
 * $Id: nccf_get_axis_datapointer.c 772 2011-06-13 15:00:28Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_axis_grp
 * Get the pointer to the axis data
 *
 * \param axisid axis ID
 * \param data pointer to the axis values
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int nccf_get_axis_datapointer(int axisid, void **data) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);

  *data = self->data;

  return status;
}
