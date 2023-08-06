/*
 * Write slices of text using a flat array index 
 * $Id: nccf_put_var_slice_text.c 513 2011-02-14 22:48:17Z dkindig $
 */

#include <stdlib.h>
#include <netcdf.h>
#include "nccf_utility_functions.h"

int 
nccf_put_var_slice_text(int ncid, int varId, int ndims, const int *dims, 
			const char *string) {

  int status = NC_NOERR;
  int blockSize = dims[ndims - 1]; 
  int i, j;
  int startIndices[ndims];
  size_t startIndicesS_t[ndims];
  int start;
  size_t counts[ndims];

  /* number of blocks to write for each dimension, {1, ...1, blockSize} */
  counts[ndims - 1] = (size_t) blockSize;

  /* number of records */
  int numberOfWrites = 1;
  for (i = 0; i < ndims - 1; ++i) {
    numberOfWrites *= dims[i];
    counts[i] = 1;
  }
	  
  /* write the data, slice by slice */
  for (i = 0; i < numberOfWrites; ++i) {
    start = i * blockSize;
    /* convert the flat index (start) into a tuple of indices (startIndices) */
    nccf_get_multi_index(ndims, dims, start, startIndices);
    for (j = 0; j < ndims; ++j) {
      startIndicesS_t[i] = (size_t) startIndices[i];
    }
    /* write the slice */
    status += nc_put_vara_text(ncid, varId, startIndicesS_t, counts, string);
  }

  return status;
}
