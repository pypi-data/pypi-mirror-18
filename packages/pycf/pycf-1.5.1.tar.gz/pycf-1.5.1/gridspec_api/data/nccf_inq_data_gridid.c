/**
 * $Id: nccf_inq_data_gridid.c 738 2011-05-06 22:26:09Z edhartnett $
 */

#include <nccf_data.h>

/**
 * \ingroup gs_data_grp
 * Get the undelying grid Id
 * \param dataid ID
 * \param gridid Id of the grid
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_data_gridid(int dataid, int *gridid){

  struct nccf_data_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);

  *gridid = self->gridid;

  return NC_NOERR;
}
