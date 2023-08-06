/*
 * $Id: nccf_inq_mosaic_coordnames.c 754 2011-05-13 20:35:24Z dkindig $
 * 
 */

#include <nccf_mosaic.h>
#include <stdio.h>
#include <string.h>

/**
 * \ingroup gs_mosaic_grp
 * Get the coordinate names.
 *
 * \param mosaicid a mosaic ID (e.g. returned by nccf_def_mosaic)
 * \param coordnames coordinate names used by grid (output)
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_coordnames( int mosaicid, char **coordnames ){

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  char *cn_ptr;
  int ndims = self->ndims, i;
  int *dims;

  nccf_varGetDataPtr( &self->coordnames, (void**)&cn_ptr );
  nccf_varGetDimsPtr( &self->coordnames, &dims );
  for( i = 0; i < ndims; i++ ){
    strcpy( coordnames[i], &cn_ptr[i*dims[1]] );
  }

  return NC_NOERR;

}
