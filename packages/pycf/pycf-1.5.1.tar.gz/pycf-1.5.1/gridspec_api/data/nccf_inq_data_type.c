/**
 * $Id: nccf_inq_data_type.c 738 2011-05-06 22:26:09Z edhartnett $
 */

#include <nccf_data.h>

/**
 * \ingroup gs_data_grp
 * Get data type.
 *
 * \param dataid data ID
 * \param dataType (output) netcdf data type
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_data_type(int dataid, nc_type *dataType){

  struct nccf_data_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);

  nccf_varGetDataType(&self->dataVar, dataType);

  return NC_NOERR;
}
