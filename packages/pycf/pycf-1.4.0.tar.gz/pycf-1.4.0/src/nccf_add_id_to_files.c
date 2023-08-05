/**
 * After generating a pseudo-random id. Add the id to the grid files, data files
 * and mosaic file as an attribute in the XXXX variable.
 *
 * I have to think how this will work. 
 *    a. Do we gen the id before creating the files? We can then put the id in
 *       the struct
 *    b. Gen the id after creating the files. Then we need a list of the files
 *       before running this routine.
 *
 * Once the attribute is populated, then we can create a host file to keep it 
 * sorted out.
 * 
 * $Id: nccf_add_id_to_files.c 513 2011-02-14 22:48:17Z dkindig $
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netcdf.h>
#include <nccf_utility_functions.h>
#include <nccf_constants.h>

int nccf_add_id_to_files(const char *id, int nfiles, const char **tile_names, 
                         const char **file_types, const char **list_o_files){
  
  char *filename, *sig;
  filename = ( char* )calloc( STRING_SIZE, sizeof( char ));
  sig      = ( char* )calloc( STRING_SIZE, sizeof( char ));
  int status = NC_NOERR, ncid, i;
  int toterr = 0;

  for( i = 0; i < nfiles; i++ ){

    sprintf( filename, "%s", list_o_files[i] );

    status = nc_open( filename, NC_WRITE, &ncid );
    if( status ) return status;
    status = nc_redef( ncid );
    toterr += abs(status);

    status = nc_put_att_text( ncid, NC_GLOBAL, CF_COORDINATES_ID, 
			      strlen( id ), id );
    toterr += abs(status);
    status = nc_put_att_text( ncid, NC_GLOBAL, CF_GRIDNAME, 
			      strlen( tile_names[i] ), tile_names[i] );
    toterr += abs(status);
    status = nc_put_att_text( ncid, NC_GLOBAL, CF_FILETYPE, 
			      strlen( file_types[i] ), file_types[i] );
    toterr += abs(status);
    
    status = nc_enddef( ncid );
    toterr += abs(status);
    status = nc_close( ncid );
    toterr += status;
  }

  free(sig);
  free(filename);

  return(toterr);
}
