/**
 * Get the static data object Ids from a host file
 *
 * $Id: nccf_inq_host_statdataids.c 823 2011-09-13 18:13:08Z dkindig $
 */

#include <nccf_host.h>
#include <string.h>
#include <stdio.h>
#include <netcdf.h>
#include <nccf_coord.h>
#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_constants.h>

int nccf_inq_host_statdataids( int hostid, const char *varname, 
                                 int readData, int *statdataids ){

  int id, status = NC_NOERR, iStat, iGrid, sdid;
  char *file;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);
  file = (char*)malloc( STRING_SIZE * sizeof(char));
  nccf_li_begin( &self->statDataFiles );
  for( iStat = 0; iStat < self->nStatDataFiles; iStat++ ){
    for( iGrid = 0; iGrid < self->nGrids; iGrid++ ){
      id = iGrid + ( self->nGrids * iStat );
      strcpy( file, nccf_li_find( &self->statDataFiles, id ));
      status = nccf_def_data_from_file( file, iGrid, varname, 
                                        readData, &sdid );
      if( status ) return status;
      statdataids[id] = sdid;
    }
  }
  free( file );

  return status;

}
