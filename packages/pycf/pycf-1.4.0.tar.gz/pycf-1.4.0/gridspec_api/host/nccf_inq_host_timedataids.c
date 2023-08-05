/**
 * Get the time data object Ids from a host file
 *
 * $Id: nccf_inq_host_timedataids.c 719 2011-04-26 17:39:51Z srinath22 $
 */

#include <nccf_host.h>
#include <string.h>
#include <stdio.h>
#include <netcdf.h>
#include <nccf_coord.h>
#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_constants.h>

int nccf_inq_host_timedataids( int hostid, const char *varname, int readData, 
                               int *timedataids ){

  int id, status = NC_NOERR, iTime, iData, iGrid, tdid;
  char *file;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);
  file = (char*)calloc( STRING_SIZE, sizeof(char));
  nccf_li_begin( &self->timeDataFiles );
  for( iTime = 0; iTime < self->nTimeSlices; iTime++ ){
    for( iData = 0; iData < self->nTimeDataFiles; iData++ ){
      for( iGrid = 0; iGrid < self->nGrids; iGrid++ ){
        id = iGrid + ( self->nGrids * ( iData + ( self->nTimeDataFiles * iTime )));
        strcpy( file, nccf_li_find( &self->timeDataFiles, id ));
        status = nccf_def_data_from_file( file, iGrid, varname, 
                                          readData, &tdid );
        if( status ) return status;
        timedataids[id] = tdid;
      }
    }
  }
  free( file );

  return status;
}
