/*
 * $Id: nccf_inq_axis_len.c 766 2011-06-06 21:18:56Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_axis_grp
 * Inquire number of elements.
 *
 * \param axisid axis ID
 * \param len number of elements 
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_axis_len(int axisid, int *len) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);

  *len = self->len;

  return status;
}
