  /********************************************************

  * Purpose :  Create a mosaic file from grid files.  Prepare the contact file
  *
  * $Id: nccf_def_mosaic.c 750 2011-05-13 19:25:37Z pletzer $
  *
  */

#include "nccf_mosaic.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <libcf_src.h>
#include <netcdf.h>
#include <nccf_grid.h>
#include <nccf_coord.h>
#include <nccf_utility_functions.h>
#include <nccf_constants.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>
#include <cflistitem.h>

struct CFLISTITEM *CFLIST_MOSAIC;

/*! \defgroup gs_mosaic_grp Mosaic connectivity
  \ingroup gridspec_grp

The mosaic file, or equivalently its representation in memory, contains
all the connectivity information between tile grids. Thus, a mosaic 
must know about its underlying grids and these must 
exist prior to the construction of a mosaic. Grid objects should not
be freed before all operations on the mosaic have been completed.

*/

/**
 * \ingroup gs_mosaic_grp
 * Define a mosaic, acts as a constructor.
 *
 * \param ngrids the number of grid files
 * \param gridids grid IDs for each grid forming the mosaic
 * \param name name of the mosaic
 * \param mosaicid (output) ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_def_mosaic( int ngrids, const int gridids[], const char *name,
                     int *mosaicid){

  struct nccf_mosaic_type *self;
  self = (struct nccf_mosaic_type *) malloc(sizeof(struct nccf_mosaic_type));

  int i;

  /* Initialize the structure */
  self->name = ( char* )calloc( STRING_SIZE, sizeof( char ));
  strcpy(self->name, name);

  self->coordnameslist   = NULL;
  self->gridnameslist    = NULL;
  self->gridtogridlist   = NULL;
  self->contactindexlist = NULL;
  nccf_li_new(&self->coordnameslist);
  nccf_li_new(&self->gridnameslist);
  nccf_li_new(&self->gridtogridlist);
  nccf_li_new(&self->contactindexlist);
  self->ncontacts = 0;
  self->ngrids    = ngrids;
  self->gridids   = ( int * )malloc( ngrids * sizeof( int ));
  self->ndims     = 0;
  self->gs_slice_format = (char*)calloc( STRING_SIZE, sizeof(char));
  strcpy( self->gs_slice_format, "C" );

  /* Populate the grid id array */
  for( i = 0; i < ngrids; i++ ) self->gridids[i] = gridids[i];

  /* add an element to the linked list */
  if (CFLIST_MOSAIC == NULL) nccf_li_new(&CFLIST_MOSAIC);

  *mosaicid = nccf_li_add( &CFLIST_MOSAIC, self );

  return NC_NOERR;

}
