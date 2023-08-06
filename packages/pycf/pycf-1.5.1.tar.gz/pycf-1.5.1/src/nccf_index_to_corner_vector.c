/**
 * $Id: nccf_index_to_corner_vector.c 373 2011-01-14 19:53:49Z pletzer $
 */

#include <netcdf.h>

int nccf_index_to_corner_vector(int index, int ndims, int vector[]) {
  /*
    Given an index in the range 3^ndims, return a unique 
    vector whose elements are -1, 0, or 1
  */

  int i, j;
  int powersOfThree;
  for (i = 0; i < ndims; ++i) {
    powersOfThree = 1;
    for (j = 0; j < i; ++j) {
      powersOfThree *= 3;
    }
    vector[i] = (index / powersOfThree % 3) - 1;
  }

  return NC_NOERR;
}
