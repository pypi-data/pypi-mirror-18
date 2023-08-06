/*
 * $Id: nccf_free_mosaic.c 918 2012-02-07 22:10:36Z pletzer $
 *
 */

#include <nccf_mosaic.h>
#include <stdlib.h>

/**
 * \ingroup gs_mosaic_grp
 * Free (destroy) a mosaic object (this will reclaim memory).
 *
 * \param mosaicid mosaic identifier
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_free_mosaic(int mosaicid) {
  
  struct nccf_mosaic_type *self;
  int index;

  /* Remove from list */
  self = nccf_li_remove(&CFLIST_MOSAIC, mosaicid);
  if( nccf_li_get_nelem( &CFLIST_MOSAIC ) == 0 )
      nccf_li_del(&CFLIST_MOSAIC);

  /* Free members */
  if (self->name) {
    free(self->name);
    self->name = NULL;
  }
  if (self->gridids) {
    free(self->gridids);
    self->gridids = NULL;
  }

  if (self->gs_slice_format) {
    free(self->gs_slice_format);
    self->gs_slice_format = NULL;
  }

  /* Free the list members */
  /* Coordinate names */ 
  nccf_li_begin( &self->coordnameslist );
  while( nccf_li_next( &self->coordnameslist )){
    index = nccf_li_get_id( &self->coordnameslist );
    char *val = nccf_li_remove( &self->coordnameslist, index );
    if(val) {
      free(val);
      val = NULL;
    }
  }

  /* Grid names */ 
  nccf_li_begin( &self->gridnameslist );
  while( nccf_li_next( &self->gridnameslist )){
    index = nccf_li_get_id( &self->gridnameslist );
    char *val = nccf_li_remove( &self->gridnameslist, index );
    if(val) {
      free(val);
      val = NULL;
    }
  }

  /* Contact index maps */ 
  nccf_li_begin( &self->contactindexlist );
  while( nccf_li_next( &self->contactindexlist )){
    index = nccf_li_get_id( &self->contactindexlist );
    char *val = nccf_li_remove( &self->contactindexlist, index );
    if(val) {
      free(val);
      val = NULL;
    }
  }

  /* Grid to grid contacts */ 
  nccf_li_begin( &self->gridtogridlist );
  while( nccf_li_next( &self->gridtogridlist )){
    index = nccf_li_get_id( &self->gridtogridlist );
    char *val = nccf_li_remove( &self->gridtogridlist, index );
    if(val) {
      free(val);
      val = NULL;
    }
  }

  /* Delete the head of each list */
  nccf_li_del( &self->coordnameslist );
  nccf_li_del( &self->gridnameslist );
  nccf_li_del( &self->contactindexlist );
  nccf_li_del( &self->gridtogridlist );

  /* Free variable */
  nccf_varDestroy(&self->contactIndex);
  nccf_varDestroy(&self->gridToGrid);
  nccf_varDestroy(&self->coordnames);
  nccf_varDestroy(&self->gridNames);
  
  /* Free object */
  free(self);
  self = NULL;

  return NC_NOERR;
}
