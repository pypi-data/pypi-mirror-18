/*
 * $Id: nccf_inq_mosaic_gridids.c 737 2011-05-06 17:48:14Z edhartnett $
 * 
 */

#include <nccf_mosaic.h>

/**
 * \ingroup gs_mosaic_grp
 * Get the grid ids.
 *
 * \param mosaicid a mosaic object handle (returned by nccf_def_mosaic)
 * \param gridids (output) array of grid unique identifiers
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_gridids(int mosaicid, int gridids[]) {

  int i;
  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  for( i = 0; i < self->ngrids; i++ ) gridids[i] = self->gridids[i];

  return NC_NOERR;
}
