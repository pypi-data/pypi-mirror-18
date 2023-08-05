/**
 * $Id: nccf_inq_coord_name.c 737 2011-05-06 17:48:14Z edhartnett $
 */

#include "nccf_coord.h"
#include <string.h>

/**
 * \ingroup gs_coord_grp
 * Fill in the coordinate name.
 *
 * \param coordid coordinate ID
 * \param coord_name The coordinate name, should be of size NC_MAX_NAME at least
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_coord_name(int coordid, char *coord_name) {

  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  strcpy(coord_name, self->coord_name);
  return NC_NOERR;
}
