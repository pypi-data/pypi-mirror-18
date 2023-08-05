/**
 * Get the number of dimensions used by data variable
 *
 * "$Id: nccf_inq_data_dims.c 1002 2016-10-04 02:39:44Z pletzer $"
 */

#include <nccf_data.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_data_grp
 * Get the dimensions of the data
 *
 * \param dataid data ID
 * \param dims dimensions (sizes) along each axis
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_data_dims(int dataid, int dims[]) {
  
  struct nccf_data_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);

  int *dimVar;
  nccf_varGetDimsPtr(&self->dataVar, &dimVar);

  int i;
  for( i = 0; i < self->ndims; i++ ){
    dims[i] = dimVar[i];
  }
  
  return NC_NOERR;
}

