/* $Id: nccf_get_grid_mask_pointer.c 738 2011-05-06 22:26:09Z edhartnett $ */

#include <nccf_grid.h>
#include <netcdf.h>
#include <nccf_coord.h>

/**
 * \ingroup gs_grid_grp
 * Get the valid data mask. 
 *
 * \param gridid grid object Id
 * \param imask_ptr pointer to the mask array
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_get_grid_mask_pointer(int gridid, int **imask_ptr) {
  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);
  *imask_ptr = self->imask;
 
  return NC_NOERR;
}
