/**
 *
 * $Id: nccf_inq_host_mosaicfilename.c 801 2011-09-11 18:58:14Z pletzer $
 */
#include <nccf_host.h>
#include <string.h>

/**
 * \ingroup gs_host_grp
 * Fill in a mosaic filename from a host file
 *
 * \param hostid the ID for the host object
 * \param mosaicfilename Mosaic filename
 * \return NC_NOERR on success
 * \author Alexander Pletzer and Dave Kindig,  Tech-X Corp
 */
int nccf_inq_host_mosaicfilename( int hostid, char *mosaicfilename ){

  int toterr = NC_NOERR;
  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  strcpy(mosaicfilename, self->mosaicFileBuffer );

  return toterr;
}
