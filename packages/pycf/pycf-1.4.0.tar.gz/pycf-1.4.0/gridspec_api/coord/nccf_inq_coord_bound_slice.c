/**
 * $Id: nccf_inq_coord_bound_slice.c 828 2011-09-14 20:05:08Z pletzer $
 */

#include "cf_config.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <nccf_coord.h>
#include <nccf_constants.h>
#include <nccf_utility_functions.h>

/**
 * \ingroup gs_coord_grp
 * Get boundary slice string.
 *
 * \param coordid coordinate ID
 * \param norm_vect an array of -1, 0, 1 elements uniquely denoting the boundary (e.g. 1,0 for north)
 * \param flip if !=0 then reverse order of beginning and end indices 
 * \param format either "Fortran" or "C"
 * \param slice (output) aka "0:11 10:11"
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_inq_coord_bound_slice(int coordid, const int norm_vect[], 
			       int flip, const char *format, 
			       char *slice) {

  int ndims, i, status;
  const char rangeSeparator[STRING_SIZE] = CF_RANGE_SEPARATOR;
  const char indexSeparator[STRING_SIZE] = CF_INDEX_SEPARATOR;
  char iBegStr[STRING_SIZE];
  char iEndStr[STRING_SIZE];
  char range[STRING_SIZE];

  status = nccf_inq_coord_ndims(coordid, &ndims);
  int dims[ndims];
  status = nccf_inq_coord_dims(coordid, dims);

  int start_indices[ndims];
  int end_indices[ndims];
  int start_indices_tmp[ndims];
  int end_indices_tmp[ndims];

  /* 
     Compute the starting/ending positions in index space
     The endingIndices are exclusive (is, ... ie(
   */
  const int exclusive = 0;
  nccf_get_start_end_bound_indices(ndims, dims, 
				   norm_vect, 
				   exclusive,
				   start_indices, 
				   end_indices);

  if (format[0] == 'F' || format[0] == 'f'){
    /* Fortran */

    /* revert order (..., k, j, i) -> (i, j, k, ...) */
    for (i = 0; i < ndims; ++i) {
      /* add one to start and end */
      start_indices_tmp[i] = start_indices[ndims - 1 - i] + 1;
      end_indices_tmp[i] = end_indices[ndims - 1 - i] + 1;
    }
    /* store */
    for (i = 0; i < ndims; ++i) {
      start_indices[i] = start_indices_tmp[i];
      end_indices[i] = end_indices_tmp[i];
    }
  }

  /* A tile is flipped relative to the other, switch the start and end indices
   * but keep the values */
  if(flip){

    /* reverse order (..., k, j, i) -> (i, j, k, ...) */
    for (i = 0; i < ndims; ++i) {
      start_indices_tmp[i] = end_indices[i];
      end_indices_tmp[i] = start_indices[i];
    }
    for (i = 0; i < ndims; ++i) {
      start_indices[i] = start_indices_tmp[i];
      end_indices[i] = end_indices_tmp[i];
    }
  }

  /* Convert the start_indices/end_indices into a string slice */
  slice[0] = '\0';
  for (i = 0; i < ndims; ++i) {
    sprintf(iBegStr, "%d", start_indices[i]);
    sprintf(iEndStr, "%d", end_indices[i]);
    strcpy(range, iBegStr);
    strcat(range, rangeSeparator);
    strcat(range, iEndStr);
    if (i < ndims - 1) {
      strcat(range, indexSeparator);
    }
    strcat(slice, range);
  }
  
  return NC_NOERR;
}
