/*
 * $Id: nccf_get_coord_data_pointer.c 757 2011-05-13 22:37:50Z pletzer $
 */

#include "nccf_coord.h"

/**
 * \ingroup gs_coord_grp
 * Get the pointer to the coordinate data.
 *
 * \param coordid coordinate ID
 * \param data (output) a pointer to the data, returned as a flat array
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_get_coord_data_pointer(int coordid, double **data) {
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  nccf_varGetDataPtr(&self->coordVar, (void **) data);
  return NC_NOERR;
}
