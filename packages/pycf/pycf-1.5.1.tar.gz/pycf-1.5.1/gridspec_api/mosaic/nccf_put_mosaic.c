/*
 * $Id: nccf_put_mosaic.c 767 2011-06-06 23:20:19Z pletzer $
 *
 */

#include <nccf_mosaic.h>
#include <string.h>
#include <stdio.h>

void nccf_set_data( int ndims, char *buffer, 
                    struct CFLISTITEM *currlist, 
                    struct nccf_var_obj *currobj ){
  int count = 0, index;
  nccf_li_begin( &currlist );
  while( nccf_li_next( &currlist )){
    index = nccf_li_get_id( &currlist);
    char *val = nccf_li_find( &currlist, index );
    strcpy( &buffer[count * STRING_SIZE], val );
    count++;
  }
  nccf_varSetDataPtr( &currobj, NC_CHAR, buffer );
}

/**
 * \ingroup gs_mosaic_grp
 * Write mosaic to netcdf file.
 *
 * \param mosaicid mosaic ID
 * \param ncid netcdf file ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */

int nccf_put_mosaic(int mosaicid, int ncid) {

  int status = NC_NOERR;
  struct nccf_mosaic_type *self;
  self = nccf_li_find( &CFLIST_MOSAIC, mosaicid );

  /* Create the dimensions for the netcdf file */
  int cndim[] = {0, 0}, gfdim[] = {0, 0}, contact_dims[2];
  cndim[0] = self->ndims;
  cndim[1] = STRING_SIZE;
  gfdim[0] = self->ngrids;
  gfdim[1] = STRING_SIZE;
  contact_dims[0] = self->ncontacts;
  contact_dims[1] = STRING_SIZE;

  const char *dimListcoordnames[] = {CF_DIMNAME_NDIMS, CF_DIMNAME_STRING};
  const char *dimListgridFiles[] = {CF_DIMNAME_NGRIDS, CF_DIMNAME_STRING};
  const char *dimNames[] = {CF_DIMNAME_NCONTACTS, CF_DIMNAME_STRING};

  /* Buffer strings */
  char *coordbuffer = (char*)calloc( self->ndims, STRING_SIZE * sizeof(char));
  char *gridbuffer = (char*)calloc( self->ngrids, STRING_SIZE * sizeof(char));
  char *contactbuffer = (char*)calloc( self->ncontacts, STRING_SIZE * sizeof(char));
  char *grid2gridbuffer = (char*)calloc( self->ncontacts, STRING_SIZE * sizeof(char));

  /* Create the Coordinate names variable */
  nccf_varCreate( &self->coordnames, CF_MOSAIC_COORDINATE_NAME );
  nccf_varSetAttribText( &self->coordnames, CF_ATTNAME_CF_TYPE_NAME, 
                        CF_GS_MOSAIC_COORDINATE_NAME );
  nccf_varSetDims( &self->coordnames, 2, cndim, dimListcoordnames );
  nccf_set_data( self->ndims, coordbuffer, self->coordnameslist, self->coordnames );

  /* Create the grid to grid contacts */
  nccf_varCreate( &self->gridToGrid, CF_MOSAIC_TILE_CONTACTS );
  nccf_varSetAttribText( &self->gridToGrid, CF_ATTNAME_CF_TYPE_NAME, 
      CF_GS_MOSAIC_TILE_CONTACTS );
  nccf_varSetDims( &self->gridToGrid, 2, contact_dims, (const char **) dimNames );
  nccf_set_data( self->ncontacts, grid2gridbuffer, self->gridtogridlist, 
                 self->gridToGrid );

  /* Create the Grid Names variable */
  nccf_varCreate( &self->gridNames, CF_MOSAIC_TILE_NAMES );
  nccf_varSetAttribText( &self->gridNames, CF_ATTNAME_CF_TYPE_NAME, 
      CF_GS_MOSAIC_TILE_NAMES );
  nccf_varSetDims( &self->gridNames, 2, gfdim, dimListgridFiles );
  nccf_set_data( self->ngrids, gridbuffer, self->gridnameslist, self->gridNames );

  /* Create the contact index map */
  nccf_varCreate( &self->contactIndex, CF_MOSAIC_CONTACT_MAP );
  nccf_varSetAttribText( &self->contactIndex, CF_ATTNAME_CF_TYPE_NAME, 
      CF_GS_MOSAIC_CONTACT_MAP );
  nccf_varSetAttribText( &self->contactIndex, CF_CONTACT_FORMAT,
      self->gs_slice_format );
  nccf_varSetDims( &self->contactIndex, 2, contact_dims, (const char **) dimNames );
  nccf_set_data( self->ncontacts, contactbuffer, self->contactindexlist, 
                 self->contactIndex );

  /* Set the save flag for each of the data pointers so they are free'd on destroy */
  self->gridNames->save = 1;
  self->gridToGrid->save = 1;
  self->coordnames->save = 1;
  self->contactIndex->save = 1;

  nccf_writeListOfVars( ncid, 1, self->coordnames );
  nccf_writeListOfVars( ncid, 1, self->gridNames );
  if( self->ncontacts > 0 ){
    nccf_writeListOfVars( ncid, 2, self->contactIndex, self->gridToGrid );
  }

//  free( coordbuffer );
//  free( gridbuffer );
//  free( contactbuffer );
//  free( grid2gridbuffer );

  return status;
}
