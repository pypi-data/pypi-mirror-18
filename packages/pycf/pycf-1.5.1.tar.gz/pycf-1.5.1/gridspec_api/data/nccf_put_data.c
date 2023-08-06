/**
 * Write structured data to file
 *
 * $Id: nccf_put_data.c 767 2011-06-06 23:20:19Z pletzer $
 */

#include "nccf_data.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>

/**
 * \ingroup gs_data_grp
 * Write object to netcdf file.
 *
 * \param dataid data ID
 * \param ncid netcdf file ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_put_data(int dataid, int ncid) {

  int status = NC_NOERR;
  struct nccf_data_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);

  // Write data to file
  if( self->numRecords == 0 ){
    status = nccf_writeListOfVars(ncid, 1, self->dataVar);
  } else {
    status = nccf_writeListOfVarData(ncid, 1, self->dataVar);
  }

  self->numRecords++;

  return status;
}
