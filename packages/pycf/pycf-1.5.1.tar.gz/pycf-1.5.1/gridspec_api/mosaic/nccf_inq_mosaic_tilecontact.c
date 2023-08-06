/*
 * $Id: nccf_inq_mosaic_tilecontact.c 756 2011-05-13 20:49:57Z dkindig $
 *
 */

#include "nccf_mosaic.h"
#include <stdio.h>
#include <string.h>
#include <libcf_src.h>

/**
 * \ingroup gs_mosaic_grp
 * Get a tile to tile contact from an index, i.e. "grid0 | grid1".
 *
 * \param mosaicid Mosaic object ID
 * \param index Contact map index
 * \param tile_contact Returned tile contacts
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_tilecontact( int mosaicid, int index, char *tile_contact){

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  char *cn_ptr;
  int *dims;
  
  nccf_varGetDataPtr( &self->gridToGrid, (void**)&cn_ptr );
  nccf_varGetDimsPtr( &self->gridToGrid, &dims );
  strcpy( tile_contact, &cn_ptr[index*dims[1]] );

  return NC_NOERR;

}

