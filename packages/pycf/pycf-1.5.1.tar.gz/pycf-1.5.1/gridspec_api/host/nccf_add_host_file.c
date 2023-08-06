/**
 * $Id: nccf_add_host_file.c 805 2011-09-12 14:55:06Z pletzer $
 */

#include <nccf_host.h>
#include <string.h>

/* Comparison function for inserting data.
 * The user knows the data type and can therefore test equality */
int item_comparison( const void *data1, const void *data2 ){
  int result;
  char *d1, *d2;
  d1 = (char*)malloc( ( strlen( (char*)data1 )+1) * sizeof( char ));
  d2 = (char*)malloc( ( strlen( (char*)data1 )+1) * sizeof( char ));

  strcpy( d1, (char*)data1 );
  strcpy( d2, (char*)data2 );

  if( strcmp( d1, d2 )  < 0) result = -1;
  if( strcmp( d1, d2 )  > 0) result =  1;
  if( strcmp( d1, d2 ) == 0) result =  0;

  free( d1 );
  free( d2 );

  return result;
}

/**
 * \ingroup gs_host_grp
 * Insert a file to the list kept in memory by host object.
 *
 * \param hostid the ID for the host object
 * \param filename name of the file, can be a data file, a grid file, or a mosaic file
 * \param force set to 1 if file should be added regardless of whether the uuid  in the file matches, otherwise uuid must match
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_add_host_file(int hostid, const char *filename, int force) {

  int nelem, ncid, status = NC_NOERR, totError = NC_NOERR, addFile = force;
  nc_type attType;
  size_t attLen;
  char *fileType = NULL, *fileTypes = NULL, *gridName = NULL;
  char *buffer = NULL;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  status = nc_open(filename, NC_NOWRITE, &ncid);
  if( status ) return status;
  totError += abs(status);

  fileTypes = (char*)calloc( STRING_SIZE, sizeof(char));

  if (!addFile) {
    status = nc_inq_att(ncid, NC_GLOBAL, CF_COORDINATES_ID, &attType, &attLen);
    if (force == 1 || ( (status == NC_NOERR) && (attType == NC_CHAR))) {
      char *coordinates_id2 = calloc(attLen, sizeof(char));
      status = nc_get_att_text(ncid, NC_GLOBAL, CF_COORDINATES_ID, 
                   coordinates_id2);
      if ( strncmp(self->coordinates_id, coordinates_id2, attLen) == 0 ) {
        addFile = 1;
      }
      free(coordinates_id2);
    }
    status = nc_inq_att(ncid, NC_GLOBAL, CF_DATA_ID, &attType, &attLen);
    if (force == 1 || ( (status == NC_NOERR) && (attType == NC_CHAR))) {
      char *data_id2 = calloc(attLen, sizeof(char));
      status = nc_get_att_text(ncid, NC_GLOBAL, CF_DATA_ID, data_id2);
      if ( strncmp(self->data_id, data_id2, attLen) == 0 ) {
        addFile = 1;
      }
      else {
        /* set to false even if coordinates_id matches */
        addFile = 0;
      }
      free(data_id2);
    }
  }

  if (addFile) {
    status = nc_get_att_text(ncid, NC_GLOBAL, CF_FILETYPE, fileTypes);

    /* Split fileType at spaces Test every instance found */
    fileType = strtok( fileTypes, " " );
    while( fileType != NULL ){
      /* A file could be of several types simulaneously. So the buffer is alloc'd
       * for each type found. */  
      if (strstr(fileType, CF_GLATT_FILETYPE_MOSAIC)) {
        buffer = (char*)calloc(STRING_SIZE, sizeof(char));
        strcpy( buffer, filename );
        self->mosaicFileBuffer = buffer;
        self->hasMosaic = 1;
      }
      if (strstr(fileType, CF_GLATT_FILETYPE_STATIC_DATA)) {
        buffer = (char*)calloc(STRING_SIZE, sizeof(char));
        strcpy( buffer, filename );
        nelem = nccf_li_get_nelem( &self->statDataFiles );
        if( nelem == 0 ) nccf_li_add(&self->statDataFiles, buffer);
        else nccf_li_insert( &self->statDataFiles, buffer, &item_comparison, 0 );
        self->nStatDataFiles++;
      }
      if (strstr(fileType, CF_GLATT_FILETYPE_TIME_DATA)) {
        buffer = (char*)calloc(STRING_SIZE, sizeof(char));
        strcpy( buffer, filename );
        nelem = nccf_li_get_nelem( &self->timeDataFiles );
        if( nelem == 0 ) nccf_li_add(&self->timeDataFiles, buffer);
        else nccf_li_insert( &self->timeDataFiles, buffer, &item_comparison, 0 );
        self->nTimeDataFiles++;
      }
      if (strstr(fileType, CF_GLATT_FILETYPE_GRID)) {
        buffer = (char*)calloc(STRING_SIZE, sizeof(char));
        strcpy( buffer, filename );
        nelem = nccf_li_get_nelem( &self->gridFiles );
        if( nelem == 0 ) nccf_li_add(&self->gridFiles, buffer);
        else nccf_li_insert( &self->gridFiles, buffer, &item_comparison, 0 );
        gridName = (char*)calloc(STRING_SIZE, sizeof( char));
        status = nc_get_att_text( ncid, NC_GLOBAL, CF_GRIDNAME, gridName ); 
        nelem = nccf_li_get_nelem( &self->gridNames );
        if( nelem == 0 ) nccf_li_add(&self->gridNames, gridName);
        else nccf_li_insert( &self->gridNames, gridName, &item_comparison, 0 );
        self->nGrids++;
      }
      fileType = strtok( NULL, " " );
    }
  }

  if( fileTypes ) free( fileTypes );

  status = nc_close(ncid);
  totError += abs(status);

  return totError;
}
