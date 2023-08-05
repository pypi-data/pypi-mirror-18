/* $Id: nccf_set_grid_validmask.c 738 2011-05-06 22:26:09Z edhartnett $ */

#include <nccf_grid.h>
#include <netcdf.h>
#include <nccf_coord.h>

/**
 * \ingroup gs_grid_grp
 * Attach valid data mask to grid. 
 *
 * \param gridid grid object Id
 * \param imask array of 1's and 0's: 1 = valid, 0 = invalid data
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_set_grid_validmask(int gridid, const int *imask) {
  int ntot, i, ierr;
  int tot_err = NC_NOERR;
  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

  /* erase */
  if (self->imask) {
    free(self->imask);
  }

  if (self->ndims > 0) {
    int dims[self->ndims];
    ierr = nccf_inq_coord_dims(self->coordids[0], dims);
    tot_err += abs(ierr);
    ntot = 1;
    for (i = 0; i < self->ndims; ++i) {
      ntot *= dims[i];
    }
    self->imask = (int *) malloc(sizeof(int) * ntot);
    for (i = 0; i < ntot; ++i) {
      self->imask[i] = imask[i];
    }
  }
 
  return tot_err;
}
