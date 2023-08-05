/*
 * API to write global attributes to a file for the gridspec convention to
 * libcf.
 *
 * $Id: nccf_put_global.c 851 2011-11-08 14:37:20Z pletzer $
 */

#include <nccf_global.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>
#include <libcf_src.h>
#include <nccf_errors.h>

int nccf_compare_values( int ncid, char *attname, const char *value );

/**
 * \ingroup gs_global_grp
 * Write the global attributes object to a file.
 *
 * \param globalId global ID
 * \param ncid NetCDF file ID created by nc_create or nc_open
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_put_global(int globalId, int ncid) {

  int status, natts, i, stat0, stat1, attid;
  int totErr = 0;
  int catchErr = NC_NOERR;

  char *attname, *attvalue;
  attname  = (char*)calloc( STRING_SIZE, sizeof(char));
  attvalue = (char*)calloc( STRING_SIZE, sizeof(char));

  /* Open the global structure. */
  struct nccf_global_type *self;
  self = nccf_li_find(&CFLIST_GLOBAL, globalId);

  /* Verify that the attributes are not in the file already. */
  nccf_inq_global_natts( globalId, &natts );
  for( i = 0; i < natts; i++ ){
    nccf_inq_global_attval( globalId, i, attname, attvalue );
    stat0 = nc_inq_attid( ncid, NC_GLOBAL, attname, &attid );

    /* Continue if an error is thrown. i.e. Attribute doesn't exist */
    if( stat0 == NC_ENOTATT ) continue;

    stat1 = nccf_compare_values( ncid, attname, attvalue );

    /* The attributes exists */
    if( stat1 != NC_NOERR ) return stat1;
  }

  free( attname );
  free( attvalue );

  /* Write global attrubutes to the file. */
  status = nccf_writeListOfVars(ncid, 1, self->global);
  if (status != NC_NOERR) {
    catchErr = status;
  }

  if (totErr != 0) {
    if (catchErr != NC_NOERR) {
      return catchErr;
    }
    else {
      return NCCF_EPUTGRID;
    }
  }
  return NC_NOERR;
}

/* This function is designed to be extended to other types */
int nccf_compare_values( int ncid, char *attname, const char *value ){

  /* Check the value */
  int stat1, result;
  nc_type type;
  size_t len;

  nc_inq_atttype( ncid, NC_GLOBAL, attname, &type );
  char *curvalue = NULL;

  nc_inq_attlen( ncid, NC_GLOBAL, attname, &len );
  curvalue = (char*) calloc(len+1, sizeof(char));
  stat1 = nc_get_att_text( ncid, NC_GLOBAL, attname, curvalue );
  if ( stat1 ) return stat1;
  result = strcmp( value, curvalue );
  free( curvalue );
  if( result == 0) return NCCF_EATTEXISTS;

  return NC_NOERR;

}
