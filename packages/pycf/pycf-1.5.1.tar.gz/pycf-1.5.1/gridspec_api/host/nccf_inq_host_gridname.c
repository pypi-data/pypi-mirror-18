/**
 * Get a grid name from a grid index.
 *
 * $Id: nccf_inq_host_gridname.c 851 2011-11-08 14:37:20Z pletzer $
 */

#include <nccf_host.h>
#include <stdio.h>
#include <string.h>

/**
* \ingroup gs_host_grp
* Return the grid name
*
* \param hostid the ID for the host object
* \param gfindx Id of grid, index varying from 0...ngrids-1
* \param gridname  grid name for Id in dataset
* \return NC_NOERR on success
* \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
*/

int nccf_inq_host_gridname( int hostid, int gfindx, char *gridname ){
  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  char *gn;
  gn = nccf_li_find(&self->gridNames, gfindx);
  strcpy( gridname, gn );

  return NC_NOERR;

}
