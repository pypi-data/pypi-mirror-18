/*
 *
 * $Id: nccf_inq_host_gridfilename.c 801 2011-09-11 18:58:14Z pletzer $
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
 * Fill in grid file name
 * 
 * \param hostid the ID for the host object
 * \param gfindx Grid file index varying from 0...ngrids-1
 * \param filename Filename for given Id from dataset (space must be pre-allocated)
 * \return NC_NOERR on success 
 * \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
 */
int nccf_inq_host_gridfilename(int hostid, int gfindx, char *filename) {

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);
  
  char *fn;
  fn = nccf_li_find(&self->gridFiles, gfindx);
  strcpy(filename, fn);

  return NC_NOERR;
}
