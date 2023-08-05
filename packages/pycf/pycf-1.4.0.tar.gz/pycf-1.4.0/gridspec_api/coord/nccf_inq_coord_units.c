/**
 * $Id: nccf_inq_coord_units.c 851 2011-11-08 14:37:20Z pletzer $
 */

#include "nccf_coord.h"
#include <string.h>

/**
 * \ingroup gs_coord_grp
 * Fill in the units attribute name.
 *
 * \param coordid coordinate ID
 * \param units The units string, should be of size NC_MAX_NAME at least 
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_coord_units(int coordid, char *units) {

  const char *units_attr;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_UNITS, 
                       (const void **)&units_attr);
  if (units_attr) {
    strcpy(units, units_attr);
  }
  else {
    strcpy(units, "");
  }
  return NC_NOERR;
}
