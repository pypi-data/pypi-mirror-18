/**
 * Add attribute
 *
 * $Id: nccf_add_coord_att.c 804 2011-09-12 03:59:08Z pletzer $
 */

#include "nccf_coord.h"

/**
 * \ingroup gs_coord_grp
 * Add attribute to object.
 *
 * \param coordid coordinate ID
 * \param name attribute name
 * \param value attribute value
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_add_coord_att(int coordid, const char *name, const char *value) {

  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  nccf_varSetAttribText(&self->coordVar, name, value);
  
  return NC_NOERR;
}
