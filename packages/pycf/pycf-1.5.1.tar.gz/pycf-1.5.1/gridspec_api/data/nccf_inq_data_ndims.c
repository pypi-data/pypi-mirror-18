/**
 * Get the number of dimensions used by data variable
 *
 * "$Id: nccf_inq_data_ndims.c 738 2011-05-06 22:26:09Z edhartnett $"
 */

#include <nccf_data.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_data_grp
 * Get the number of dimensions of the data
 *
 * \param dataid data ID
 * \param nDataDims number of dimensions
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_data_ndims( int dataid, int *nDataDims ){
  
   struct nccf_data_type *self;
   self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);

   *nDataDims = self->ndims;

  return NC_NOERR;

}
