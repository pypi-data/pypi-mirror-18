/*
 *
 * $Id: nccf_inq_host_ntimeslices.c 809 2011-09-12 19:45:48Z dkindig $
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
 * Get the number of time slices per time data file
 *
 * \param hostid the ID for the host object
 * \param ntimeslices number of time slices per file
 * \return NC_NOERR on success
 * \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
 */

int nccf_inq_host_ntimeslices(int hostid, int *ntimeslices) {
  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  *ntimeslices = self->nTimeSlices;

  return NC_NOERR;
}
