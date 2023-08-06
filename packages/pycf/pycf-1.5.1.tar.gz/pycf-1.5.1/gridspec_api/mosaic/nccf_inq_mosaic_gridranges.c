/**
 *  $Id: nccf_inq_mosaic_gridranges.c 941 2016-09-05 03:00:31Z pletzer $
 *
 */

#include <nccf_mosaic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <nccf_errors.h>

/* Utility function */
int nccf_remove_whitespace( char *tmpstr, char *output ){

  int i = 0;
  char *p = tmpstr;
  while(*p)
  {
     if(*p != ' ')
        output[i++] = *p;
     p++;
  }
  output[i] = 0;

  return 0;
}

/* Find the grid id */
//int nccf_find_gridid( const char *gridname, const char *gridnamesbuffer,
//                        int gridids[], int ngrids ){
int nccf_find_gridid(const char *gridname, struct CFLISTITEM *list,
                      int gridids[], int ngrids){

  int iGrid, result, gridid = NC_EBADID;
  char *gn, *tmpname;
  tmpname = (char*)malloc(STRING_SIZE * sizeof(char));
  gn      = (char*)malloc(STRING_SIZE * sizeof(char));
  strcpy( gn, gridname );
  nccf_remove_whitespace(gn, tmpname);
  for (iGrid = 0; iGrid < ngrids; ++iGrid){
//    result = strcmp( tmpname, &gridnamesbuffer[iGrid * STRING_SIZE] );
    result = strcmp(tmpname, nccf_li_find( &list, iGrid));
    if( result == 0 ){
      gridid = gridids[iGrid];
      break;
    }
  }

  free(gn);
  free(tmpname);

  return gridid;
}

/**
 * \ingroup gs_mosaic_grp
 * Get contact indices from a given contact.
 *
 * \param mosaicid mosaic object ID (returned by nccf_def_mosaic)
 * \param index contact index
 * \param gridid0 (output) first grid in contact
 * \param gridid1 (output) second grid in contact
 * \param grid0_beg_ind (output) begin indices for the coordinates on the first grid
 * \param grid0_end_ind (output) end indices for the coordinates on the first grid
 * \param grid1_beg_ind (output) begin indices for the coordinates on the second grid
 * \param grid1_end_ind (output) end indices for the coordinates on the second grid
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_mosaic_gridranges( int mosaicid, int index,
                                 int *gridid0, int *gridid1,
                                 int grid0_beg_ind[], int grid0_end_ind[],
                                 int grid1_beg_ind[], int grid1_end_ind[]){

  int ndims, ngrids;

  /* Search Strings and delimieters for sscanf*/
  char *contactMapStr, *tileContactStr, *contactIndex, *gridToGrid;
  int j, iIdx, iDim, cnt;
  char *str1, *str2, *token, *subtoken, *saveptr1, *saveptr2;

  struct nccf_mosaic_type *self;
  self = nccf_li_find(&CFLIST_MOSAIC, mosaicid);

  ndims = self->ndims;
  ngrids = self->ngrids;

  tileContactStr   = (char*)calloc( STRING_SIZE, sizeof( char ));
  contactMapStr  = (char*)calloc( STRING_SIZE, sizeof( char ));

  /* Read the grids */
  nccf_varGetDataPtr( &self->gridToGrid, (void **) &gridToGrid );
  nccf_varGetDataPtr( &self->contactIndex, (void **) &contactIndex );

  /* Read the string */
//  strcpy( contactMapStr,  &contactIndex[index * STRING_SIZE] );
//  strcpy( tileContactStr, &gridToGrid[index * STRING_SIZE] );
  sprintf( contactMapStr, "%s", &contactIndex[index * STRING_SIZE] );
  sprintf( tileContactStr, "%s", &gridToGrid[index * STRING_SIZE] );

  /* Split the two tiles apart into separate strings */
  char *tile_separator;
  tile_separator = (char*)calloc( STRING_SIZE, sizeof( char ));

  char *tmpstr;
  tmpstr = (char*)malloc( strlen(CF_TILE_SEPARATOR)+1);
  strcpy( tmpstr, CF_TILE_SEPARATOR );
  if(strchr( tmpstr, ' ' ) != NULL ){
    /* CF_TILE_SEPARATOR has a space */
    nccf_remove_whitespace( tmpstr, tile_separator );
  } else {
    /* Use the separator as is */
    strcpy( tile_separator, CF_TILE_SEPARATOR );
  }
  /* Clean up */
  free( tmpstr );

  /* Find the grid Ids from the tile contact string */
  for( j = 1, str1 = tileContactStr; ; j++, str1 = NULL ){
    
    /* Split the index string */
    token = strtok_r( str1, tile_separator, &saveptr1 );
    if( token == NULL )
      break;

    /* Get the grid Id from self */
    if( j == 1 ) *gridid0 = nccf_find_gridid( token, self->gridnameslist, 
                                              self->gridids, ngrids );
    if( j == 2 ) *gridid1 = nccf_find_gridid( token, self->gridnameslist, 
                                              self->gridids, ngrids );
  }

  /* Create the subtoken string by concatenating the
   * INDEX and RANGE separators */
  char *range_index_sep;
  int len = strlen( CF_INDEX_SEPARATOR ) + strlen( CF_RANGE_SEPARATOR ) + 1;
  range_index_sep = (char*)malloc( len * sizeof(char));
  strcpy( range_index_sep, CF_RANGE_SEPARATOR );
  strcat( range_index_sep, CF_INDEX_SEPARATOR );

  /* Loop over the contactMapStr and split on the CF_TILE_SEPARATOR
   * Then split each Dimension to get the beginning and end indices */
  iDim = 0;
  cnt = 0;
  for( j = 1, str1 = contactMapStr; ; j++, str1 = NULL ){
    
    /* Split the index string */
    token = strtok_r( str1, tile_separator, &saveptr1 );
    if( token == NULL )
      break;

    /* Find the indices. Increment the dimension only when both indices have 
     * been retrieved */
    for( str2 = token; ; str2 = NULL ){

      /* iIdx = 0, 1 --> beg, end */
      iIdx = (cnt % 2);

      /* iDim = 0, 1...ndims at contact between 2 tiles */
      iDim = ( cnt / 2 ) % ndims;

      subtoken = strtok_r( str2, range_index_sep, &saveptr2 );
      if( subtoken == NULL )
        break;

      if( j == 1 ){
        if(iIdx == 0) grid0_beg_ind[iDim] = atoi(subtoken);
        if(iIdx == 1) grid0_end_ind[iDim] = atoi(subtoken);
      }
      if( j == 2 ){
        if(iIdx == 0) grid1_beg_ind[iDim] = atoi(subtoken);
        if(iIdx == 1) grid1_end_ind[iDim] = atoi(subtoken);
      }
      cnt++;
    }
  }

  free( tile_separator );
  free( tileContactStr );
  free( contactMapStr );
  free( range_index_sep );

  /* Make sure the cnt has reached 
   * cnt = (beg, end) * (tile contact0, tile contact 1)* ndims */
  if (cnt !=  2 * 2 * ndims ) {
    return NCCF_EPARSERANGES;
  }
  else {
    return NC_NOERR;
  }
}
