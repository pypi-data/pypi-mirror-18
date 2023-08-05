/*
 *
 * $Id: nccf_inq_host_ngrids.c 813 2011-09-12 20:54:25Z pletzer $
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
 * Get the number of grid files from a host file
 *
 * \param hostid the ID for the host object
 * \param ngrids  number of grids
 * \return NC_NOERR on success
 * \author Dave Kindig and Alexander Pletzer, Tech-X Corp
 */

int nccf_inq_host_ngrids(int hostid, int *ngrids){

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  *ngrids = self->nGrids;

  return NC_NOERR;
}
