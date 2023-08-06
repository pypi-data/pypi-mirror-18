/*
 * $Id: nccf_inq_mosaic_gridname.c 755 2011-05-13 20:47:11Z dkindig $
 * 
 */

#include <nccf_mosaic.h>
#include <stdio.h>

/**
 * \ingroup gs_mosaic_grp
 * Get the i-th gridname.
 *
 * \param mosaicid mosaic ID
 * \param index index of grid
 * \param gridname (output) The grid name
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_gridname(int mosaicid, int index, char *gridname){

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  gridname = (char*)nccf_li_find( &self->gridnameslist, index );

  return NC_NOERR;
}
