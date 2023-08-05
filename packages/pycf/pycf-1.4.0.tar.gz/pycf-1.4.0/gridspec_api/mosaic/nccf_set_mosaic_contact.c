/********************************************************
  * Set the contact indices for a given contact.
  *
  * $Id: nccf_set_mosaic_contact.c 981 2016-09-14 08:23:44Z pletzer $
  *
  */

#include <stdio.h>
#include <string.h>
#include "nccf_mosaic.h"
#include <libcf_src.h>

/* Convert the start_indices/end_indices into a string slice */
void nccf_make_slice( int ndims, int bind[], int eind[], char *slice ){
  char *iBegStr, *iEndStr;
  char range[STRING_SIZE];
  int i;

  strcpy( slice, "\0" );
  iBegStr = (char*)calloc( STRING_SIZE, sizeof(char) );
  iEndStr = (char*)calloc( STRING_SIZE, sizeof(char) );

  for (i = 0; i < ndims; ++i) {
    sprintf(iBegStr, "%d", bind[i]);
    sprintf(iEndStr, "%d", eind[i]);
    strcpy(range, iBegStr);
    strcat(range, CF_RANGE_SEPARATOR);
    strcat(range, iEndStr);
    if (i < ndims - 1) {
      strcat(range, CF_INDEX_SEPARATOR);
    }
    strcat(slice, range);
  }

  free( iBegStr );
  free( iEndStr );
}

int nccf_item_comparison( const void *A, const void *B ){
  int result;
  char *string1, *string2;
  string1 = (char*)calloc( strlen((char*)A )+1, sizeof(char) );
  string2 = (char*)calloc( strlen((char*)B )+1, sizeof(char) );
  strcpy( string1, (char*)A );
  strcpy( string2, (char*)B );

  if( strcmp( string1, string2 ) <  0 ) result = -1;
  if( strcmp( string1, string2 ) >  0 ) result =  1;
  if( strcmp( string1, string2 ) == 0 ) result =  0;

  free( string1 );
  free( string2 );

  return result;

}

void nccf_local_pop_list( struct CFLISTITEM *list, char *string ){
  if( nccf_li_get_nelem( &list ) == 0 ){
    nccf_li_add( &list, string );
  }
  else{
    nccf_li_insert( &list, string, &nccf_item_comparison, 1 );
  }
}

/**
 * \ingroup gs_mosaic_grp
  * Set the contact indices for a given contact.
 *
 * \param mosaicid Mosaic object ID
 * \param ndims Number of dimensions
 * \param grididA The grid id for the first grid ( tile )
 * \param grididB The grid id for the second grid ( tile )
 * \param gridA_beg_ind Vector containing ndims of grid id A beginning indices
 * \param gridB_beg_ind Vector containing ndims of grid id B beginning indices
 * \param gridA_end_ind Vector containing ndims of grid id A ending indices
 * \param gridB_end_ind Vector containing ndims of grid id B ending indices
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_set_mosaic_contact( int mosaicid, int ndims, 
         int grididA, int grididB,
         int gridA_beg_ind[], int gridA_end_ind[], 
         int gridB_beg_ind[], int gridB_end_ind[]){


  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);
  self->ndims = ndims;

  int status = NC_NOERR, i;
  char *sliceA, *sliceB, *contactMap, *gridMap;
  char *gridnameA, *gridnameB;
  char **coordnames = NULL;
  char *coordname = NULL;

  /* Build the contact index map */
  sliceA = (char *) calloc( STRING_SIZE, sizeof(char));
  sliceB = (char *) calloc( STRING_SIZE, sizeof(char));

  nccf_make_slice( ndims, gridA_beg_ind, gridA_end_ind, sliceA);
  nccf_make_slice( ndims, gridB_beg_ind, gridB_end_ind, sliceB);

  contactMap = (char *) calloc( STRING_SIZE, sizeof(char));
  sprintf( contactMap, "%s%s%s", sliceA, CF_TILE_SEPARATOR, sliceB );

  /* Build tile contact map */
  gridnameA = (char *) calloc( STRING_SIZE, sizeof(char));
  gridnameB = (char *) calloc( STRING_SIZE, sizeof(char));
  if ((status = nccf_inq_grid_name( grididA, gridnameA))) ERR;
  if ((status = nccf_inq_grid_name( grididB, gridnameB))) ERR;

  gridMap = (char*)calloc( STRING_SIZE, sizeof(char) );
  sprintf( gridMap, "%s%s%s", gridnameA, CF_TILE_SEPARATOR, gridnameB);

  /* Get the coordinate names */
  status = nccf_inq_grid_ndims( grididA, &ndims );
  coordnames = (char **) malloc(ndims * sizeof(char *));
  for (i = 0; i < ndims; ++i) {
    coordnames[i] = (char *) calloc(STRING_SIZE, sizeof(char));
  }
  //coordnames = (char *) calloc( ndims, STRING_SIZE * sizeof(char) );
  //status = nccf_inq_grid_coordnames( grididA, coordnames );
  status = nccf_inq_grid_coordnames(grididA, coordnames);

  /* Add the maps to the appropriate list in mosaic */
  for( i = 0; i < ndims; i++ ){
    coordname = (char *) calloc(STRING_SIZE, sizeof(char));
    strcpy(coordname, coordnames[i]);
    nccf_local_pop_list(self->coordnameslist, coordname);
  }
  nccf_local_pop_list(self->gridnameslist, gridnameA);
  nccf_local_pop_list(self->gridnameslist, gridnameB);
  nccf_local_pop_list(self->contactindexlist, contactMap);
  nccf_local_pop_list(self->gridtogridlist, gridMap);

  /* Update the number of contacts */
  self->ncontacts++;

  for (i = 0; i < ndims; ++i) {
    free(coordnames[i]);
  }
  free(coordnames);
  free(sliceA);
  free(sliceB);

  return status;

}
