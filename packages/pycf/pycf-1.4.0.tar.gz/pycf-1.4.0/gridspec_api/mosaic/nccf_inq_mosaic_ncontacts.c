/*
 * $Id: nccf_inq_mosaic_ncontacts.c 737 2011-05-06 17:48:14Z edhartnett $
 * 
 */

#include <nccf_mosaic.h>

/**
 * \ingroup gs_mosaic_grp
 * Inquire the number of contacts from the mosaic. 
 *
 * \param mosaicid mosaic file ID
 * \param ncontacts number of contacts
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_ncontacts(int mosaicid, int *ncontacts) {

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  *ncontacts = self->ncontacts;

  return NC_NOERR;
}
