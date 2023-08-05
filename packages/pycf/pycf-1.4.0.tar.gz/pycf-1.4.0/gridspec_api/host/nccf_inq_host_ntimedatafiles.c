/*
 *
 * $Id: nccf_inq_host_ntimedatafiles.c 810 2011-09-12 20:11:37Z dkindig $
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
 * Get the number of time data files from host file
 *
 * \param hostid the ID for the host object
 * \param ntimedatafiles number of time data files
 * \return NC_NOERR on success
 * \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
 */

int nccf_inq_host_ntimedatafiles(int hostid, int *ntimedatafiles) {
  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  *ntimedatafiles = self->nTimeDataFiles;

  return NC_NOERR;
}
