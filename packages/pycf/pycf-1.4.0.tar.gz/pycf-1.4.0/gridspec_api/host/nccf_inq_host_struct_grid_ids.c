/**
 * Get the grid object Ids from a host file
 *
 * $Id: nccf_inq_host_struct_grid_ids.c 977 2016-09-12 04:56:44Z pletzer $
 */

#include <nccf_host.h>
#include <string.h>
#include <stdio.h>
#include <netcdf.h>
#include <nccf_coord.h>
#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_constants.h>

int nccf_inq_host_struct_grid_ids( int hostid, int ndims, 
                                   char **coordNames, int gridids[] ){

  int id, status = NC_NOERR, i, gid;
  char *file;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);
  file = (char*)malloc( STRING_SIZE * sizeof(char));
  i = 0;
  nccf_li_begin( &self->gridFiles );
  while( nccf_li_next( &self->gridFiles )){
    id = nccf_li_get_id( &self->gridFiles );
    strcpy( file, nccf_li_find( &self->gridFiles, id ));
    status = nccf_def_grid_from_file( file, ndims, 
                         (const char**)coordNames, &gid );
    if( status ) return status;
    gridids[i] = gid;
    i++;
  }
  free( file );

  return status;
}
