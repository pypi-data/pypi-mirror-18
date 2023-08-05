/**
 * $Id: nccf_inq_mosaic_contactmap.c 753 2011-05-13 20:31:50Z pletzer $
 */

#include "nccf_mosaic.h"
#include <stdio.h>
#include <string.h>
#include <libcf_src.h>

/**
 * \ingroup gs_mosaic_grp
 * Get contact map for a given index from a mosaic object.
 *
 * \param mosaicid Mosaic object ID
 * \param index Contact map index
 * \param contact_map Returned contact map string 
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_contactmap( int mosaicid, int index, char *contact_map){

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  char *cn_ptr;
  int *dims;
  
  nccf_varGetDataPtr( &self->contactIndex, (void**)&cn_ptr );
  nccf_varGetDimsPtr( &self->contactIndex, &dims );
  strcpy( contact_map, &cn_ptr[index*dims[1]] );

  return NC_NOERR;

}
