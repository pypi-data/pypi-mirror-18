/*
 * $Id: nccf_inq_mosaic_tileseparator.c 756 2011-05-13 20:49:57Z dkindig $
 *
 */
 
#include "nccf_mosaic.h"
#include <stdio.h>
#include <string.h>
#include <libcf_src.h>
#include "nccf_constants.h"

/**
 * \ingroup gs_mosaic_grp
 * Get the separator for the contact_map and tile_contacts.
 *
 * \param tile_separator Returned string CF_TILE_SEPARATOR
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_tileseparator( char *tile_separator){

  strcpy( tile_separator, CF_TILE_SEPARATOR );

  return NC_NOERR;

}


