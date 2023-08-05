/**
 * API retrieve host from a hostfile.
 *
 * "$Id: nccf_def_host_from_file.c 941 2016-09-05 03:00:31Z pletzer $"
 */

#include "nccf_host.h"
#include <stdio.h>
#include <string.h>

#include <libgen.h>
#include <netcdf.h>
#include "nccf_global.h"
#include "nccf_varObj.h"
#include "nccf_errors.h"

/* Some methods used for gathering variables - Currently commented out 
 * Keeping for possible future use */
int nccf_var_in_list( const char *varname, struct CFLISTITEM *var_info );
int nccf_pop_variable_list( const char *filename, const char *gst_cat,
                            struct nccf_host_type *tmp );


/******************************************************************/
/**
 * \ingroup gs_host_grp
 * Define (construct) a host file from a netcdf file.
 *
 * \param filename the host filename
 * \param hostid (output) the ID for the host object
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_host_from_file(const char *filename, int *hostid){

  int ncid, status, igrid, ifile, ii, nFiles, test;
  int *dims, nDims;
  char* file_type, *buffer, *buffe2, **coordNames;
  int mosaicid, nCoordDims;

  char *hostpath, *slash = "/", *hp;
  char *new_path, *fn;

  fn = (char*)calloc( STRING_SIZE, sizeof(char));
  strncpy(fn, filename, strlen( filename ));
  hp = dirname( fn );
  hostpath = (char*)calloc(STRING_SIZE, sizeof(char));
  strcpy(hostpath, hp);
  strcat(hostpath, slash);

  status = nc_open( filename, NC_NOWRITE, &ncid );
  if (status != NC_NOERR) return status;

  struct nccf_host_type *self;
  self = ( struct nccf_host_type *)malloc( sizeof( struct nccf_host_type ));

  /* Initialize structures */
  self->gridFiles = NULL;
  self->gridNames = NULL;
  self->timeDataFiles = NULL;
  self->statDataFiles = NULL;
  self->variables = NULL;
  self->nVars = 0;
  self->mosaicFileBuffer = NULL;
  self->coordinates_id   = NULL;
  self->data_id          = NULL;
  self->hasMosaic = 0;
  self->nGrids = 0;
  self->nStatDataFiles = 0;
  self->nTimeDataFiles = 0;
  self->nTimeSlices = 0;
  self->uuid = NULL;

  struct nccf_var_obj *mosaicFile_var_obj;
  struct nccf_var_obj *gridFile_var_obj;
  struct nccf_var_obj *gridName_var_obj;
  struct nccf_var_obj *statData_var_obj;
  struct nccf_var_obj *timeData_var_obj;

  /* Initialize the list objects */
  nccf_li_new( &self->gridFiles );
  nccf_li_new( &self->gridNames );
  nccf_li_new( &self->timeDataFiles );
  nccf_li_new( &self->statDataFiles );
  nccf_li_new( &self->variables );

  /* Get the global attributes */
  int globalId;
  nccf_def_global_from_file( filename, &globalId );
  file_type = (char*)calloc( STRING_SIZE, sizeof(char));
  self->coordinates_id = (char*)calloc( 36+1, sizeof(char));
  self->data_id        = (char*)calloc( 36+1, sizeof(char));
  status = nccf_inq_global_att( globalId, CF_FILETYPE, file_type );
  status = nccf_inq_global_att( globalId, CF_COORDINATES_ID, self->coordinates_id );
  status = nccf_inq_global_att( globalId, CF_DATA_ID, self->data_id );
  status = nccf_free_global( globalId );
  test = strcmp( file_type, CF_GLATT_FILETYPE_HOST );
  free( file_type );
  if( test != 0 ){
    return NCCF_ENOTHOSTFILE;
  }

  /* Get the mosaic filename */
  char *mosaicFileBuffer;
  new_path = (char*)calloc( STRING_SIZE, sizeof(char));
  strcpy( new_path, hostpath );
  nccf_varCreateFromFile( &mosaicFile_var_obj, CF_HOST_MOSAIC_FILENAME, 
                          ncid, 1, 0 );
  nccf_varGetDataPtr( &mosaicFile_var_obj, (void**)&mosaicFileBuffer );
  self->mosaicFileBuffer = (char*)calloc( STRING_SIZE, sizeof(char));
  strcpy( self->mosaicFileBuffer, new_path );
  strcat( self->mosaicFileBuffer, mosaicFileBuffer );
  nccf_varDestroy( &mosaicFile_var_obj );

  /* Get the mosaic coordinate names */
  nccf_def_mosaic_from_file( self->mosaicFileBuffer, "", &mosaicid );
  nccf_inq_mosaic_ndims( mosaicid, &nCoordDims );
  coordNames = (char**)calloc( nCoordDims, STRING_SIZE * sizeof(char*));
  for( ii = 0; ii < nCoordDims; ii++ )
    coordNames[ii] = (char*)calloc( STRING_SIZE, sizeof(char));
  nccf_inq_mosaic_coordnames( mosaicid, coordNames );
  nccf_free_mosaic( mosaicid );

  /* Get the grid files */
  nccf_varCreateFromFile( &gridFile_var_obj,
                          CF_HOST_TILE_FILENAMES, ncid, 1, 0 );
  nccf_varGetNumDims( &gridFile_var_obj, &nDims );
  nccf_varCreateFromFile( &gridName_var_obj,
                          CF_MOSAIC_TILE_NAMES, ncid, 1, 0 );
  if( nDims != 0 ){
    char *gridFileBuffer, *gridNameBuffer;
    nccf_varGetDimsPtr( &gridFile_var_obj, &dims );
    self->nGrids = dims[0];
    nccf_varGetDataPtr( &gridFile_var_obj, (void**)&gridFileBuffer );
    nccf_varGetDataPtr( &gridName_var_obj, (void**)&gridNameBuffer );

    /* Add the grid name and file to separate lists */
    for( igrid = 0; igrid < self->nGrids; igrid++ ){
      buffe2 = (char*)calloc( dims[1], sizeof(char));
      strcpy( buffe2, &gridNameBuffer[igrid * dims[1]] );
      nccf_li_add( &self->gridNames, buffe2 );

      buffer = (char*)calloc( dims[1], sizeof(char));
      strcpy( new_path, hostpath );
      strcpy( buffer, new_path );
      strcat( buffer, &gridFileBuffer[igrid * dims[1]] );
      nccf_li_add( &self->gridFiles, buffer );

    }
  }
  nccf_varDestroy( &gridFile_var_obj );
  nccf_varDestroy( &gridName_var_obj );

  /* Get the static data */
  nccf_varCreateFromFile( &statData_var_obj,
                          CF_HOST_STATDATA_FILENAME, ncid, 1, 0 );
  nccf_varGetNumDims( &statData_var_obj, &nDims );

  /* Dont process the variable if it has no dimensions */
  if( nDims != 0 ){
    char *statFileBuffer;
    nccf_varGetDimsPtr( &statData_var_obj, &dims );
    nccf_varGetDataPtr( &statData_var_obj, (void**)&statFileBuffer );

    /* Get the number of files from nStats * nGrids */
    self->nStatDataFiles = dims[0];
    if( dims[1] != (self->nGrids) ) return NCCF_ENGRIDMISMATCH;
    nFiles = 1;
    for( ifile = 0; ifile < nDims-1; ifile++ ) nFiles *= dims[ifile];
    for( ifile = 0; ifile < nFiles; ifile++ ){
      buffer = (char*)calloc( dims[nDims-1], sizeof(char));
      strcpy( buffer, new_path);
      strcat( buffer, &statFileBuffer[ifile * dims[nDims-1]] );
      nccf_li_add( &self->statDataFiles, buffer );

      /* Add variables to var_information->varname*/
//      nccf_pop_variable_list( buffer, "static", self );

    }
  } else {
    self->nStatDataFiles = 0;
  }
  nccf_varDestroy( &statData_var_obj );

  /* Get the time data */
  nccf_varCreateFromFile( &timeData_var_obj,
                          CF_HOST_TIMEDATA_FILENAME, ncid, 1, 0 );
  nccf_varGetNumDims( &timeData_var_obj, &nDims );
  if( nDims != 0 ){
    char *timeFileBuffer;
    nccf_varGetDimsPtr( &timeData_var_obj, &dims );
    nccf_varGetDataPtr( &timeData_var_obj, (void**)&timeFileBuffer );

    /* Get the number of files from nTimes * nVars* nGrids */
    self->nTimeSlices = dims[0];
    self->nTimeDataFiles = dims[1];
    if( dims[2] != self->nGrids ) return NCCF_ENGRIDMISMATCH;
    nFiles = 1;
    for( ifile = 0; ifile < nDims-1; ifile++ ){
      nFiles *= dims[ifile];
    }
    for( ifile = 0; ifile < nFiles; ifile++ ){
      buffer = (char*)calloc( dims[nDims-1], sizeof(char));
      strcpy( buffer, new_path);
      strcat( buffer, &timeFileBuffer[ifile * dims[nDims-1]] );
      nccf_li_add( &self->timeDataFiles, buffer );

      /* Add variables to var_information->varname*/
//      nccf_pop_variable_list( buffer, "time", self );

    }
  } else {
    self->nTimeDataFiles = 0;
  }
  nccf_varDestroy( &timeData_var_obj );

  status = nc_close( ncid );
  for( ii = 0; ii < nCoordDims; ii++ ) free( coordNames[ii] );
  free( coordNames );

  /* Return an ID */
  nccf_li_new( &CFLIST_HOST );
  //if( CFLIST_HOST == NULL ) nccf_li_new( &CFLIST_HOST );
  *hostid = nccf_li_add( &CFLIST_HOST, self );

  /* Clean up */
  free( hostpath );
  free( fn );
  free( new_path );
  return status;
}

int nccf_var_in_list( const char *varname, struct CFLISTITEM *var_info ){
  int varNotInList = 0;
  int index;
  struct var_information *vi;

  nccf_li_begin( &var_info );
  while( nccf_li_next( &var_info )){
    index = nccf_li_get_id( &var_info );
    vi = nccf_li_find( &var_info, index );
    if( strcmp( vi->varname, varname ) == 0 ){
      return 1;
    }
  }

  return varNotInList;
}

int nccf_pop_variable_list( const char *filename, const char *gst_cat,
                            struct nccf_host_type *tmp ){

    struct var_information *var_info;
    int ncid2, nlocal, ivar, varInList, status = NC_NOERR, id;
    char *varname;

    /* Add variables to var_information->varname*/
    if(( status = nc_open( filename, NC_NOWRITE, &ncid2 ))) return status;
    if(( status = nc_inq_nvars( ncid2, &nlocal ))) return status;

    varname = (char*)calloc( STRING_SIZE, sizeof(char));
    for( ivar = 0; ivar < nlocal; ivar++ ){
      if(( status = nc_inq_varname( ncid2, ivar, varname ))) return status;

      varInList = nccf_var_in_list( varname, tmp->variables );

      struct nccf_var_obj *file_var_obj;

      if( varInList == 0 ){

        /* Add the variable to the var_info list */
        struct var_information *var_info =
            (struct var_information*)malloc(sizeof(struct var_information));
        var_info->varname = (char*)calloc( STRING_SIZE, sizeof(char));
        strcpy( var_info->varname, varname );
        var_info->grid_stat_time_cat = (char*)calloc( STRING_SIZE, sizeof(char));
        strcpy( var_info->grid_stat_time_cat, gst_cat );

        nccf_li_new( &var_info->file_var_obj );

        /* Read the variable without getting the data */
        int readData = 0;
        nccf_varCreateFromFile( &file_var_obj, varname, ncid2, readData, 0 );
        nccf_varSetVarName( &file_var_obj, filename );

        nccf_li_add( &var_info->file_var_obj, file_var_obj );
        nccf_li_add( &tmp->variables, var_info );
        tmp->nVars++;
      } else {

        /* Read the variable without getting the data */
        int readData = 0;
        nccf_varCreateFromFile( &file_var_obj, varname, ncid2, readData, 0 );
        nccf_varSetVarName( &file_var_obj, filename );

        nccf_li_begin( &tmp->variables );
        while( nccf_li_next( &tmp->variables )){
          id = nccf_li_get_id( &tmp->variables );
          var_info =
            (struct var_information *)nccf_li_find( &tmp->variables, id );
          if( strcmp( var_info->varname, varname ) == 0 ){
            nccf_li_add( &var_info->file_var_obj, file_var_obj );
          }
        }
      }

      char *gridName;
      gridName = (char*)calloc( STRING_SIZE, sizeof(char));
      nc_get_att_text( ncid2, NC_GLOBAL, CF_GRIDNAME, gridName);
      nccf_varSetAttribText(&file_var_obj, CF_GRIDNAME, gridName);
      free(gridName);

    }
    free( varname );

    if((status = nc_close( ncid2 ))) return status;

    return status;
}
