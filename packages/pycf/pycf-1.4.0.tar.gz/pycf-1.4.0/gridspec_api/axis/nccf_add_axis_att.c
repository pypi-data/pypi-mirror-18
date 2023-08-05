/*
 * $Id: nccf_add_axis_att.c 766 2011-06-06 21:18:56Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_axis_grp
 * Add attribute to axis.
 *
 * \param axisid axis ID
 * \param name name of attribute
 * \param value value of attribute
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int nccf_add_axis_att(int axisid, const char *name, const char *value) {

  int status = NC_NOERR;
  struct nccf_axis_type *self;
  self = nccf_li_find(&CFLIST_AXIS, axisid);
  nccf_varSetAttribText(&self->axisVar, name, value);

  return status;
}
