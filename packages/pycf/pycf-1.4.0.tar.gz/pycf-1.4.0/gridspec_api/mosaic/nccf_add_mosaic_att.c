/**
 * Add attribute
 *
 * $Id: nccf_add_mosaic_att.c 737 2011-05-06 17:48:14Z edhartnett $
 */

#include "nccf_mosaic.h"

/**
 * \ingroup gs_mosaic_grp
 * Add an attribute to a mosaic.
 *
 * \param mosaicid mosaic ID
 * \param name name of the attribute to add
 * \param value value of the attribute
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_add_mosaic_att(int mosaicid, const char *name, const char *value) {

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);
  nccf_varSetAttribText(&self->gridToGrid, name, value);
  
  return NC_NOERR;
}
