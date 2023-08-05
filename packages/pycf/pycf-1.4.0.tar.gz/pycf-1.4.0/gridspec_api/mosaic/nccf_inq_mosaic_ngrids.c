/*
 * $Id: nccf_inq_mosaic_ngrids.c 737 2011-05-06 17:48:14Z edhartnett $
 * 
 */

#include <nccf_mosaic.h>

/**
 * \ingroup gs_mosaic_grp
 * Get the number of grids.
 *
 * \param mosaicid a mosaic ID (e.g. returned by nccf_def_mosaic)
 * \param ngrids number of grids (output)
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_ngrids(int mosaicid, int *ngrids) {

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  *ngrids = self->ngrids;

  return NC_NOERR;
  
}
