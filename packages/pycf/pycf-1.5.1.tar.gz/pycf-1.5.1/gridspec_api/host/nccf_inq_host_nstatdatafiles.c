/*
 *
 * $Id: nccf_inq_host_nstatdatafiles.c 823 2011-09-13 18:13:08Z dkindig $
 */

#include <nccf_host.h>
#include <string.h>
#include <stdio.h>
#include <netcdf.h>
#include <nccf_coord.h>
#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_constants.h>

/**
 * \ingroup gs_host_grp
 * Get the number of static data files from host file
 *
 * \param hostid the ID for the host object
 * \param nstatdatafiles number of static data files
 * \return NC_NOERR on success
 * \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
 */

int nccf_inq_host_nstatdatafiles( int hostid, int *nstatdatafiles ){
  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  *nstatdatafiles = self->nStatDataFiles;

  return NC_NOERR;
}
