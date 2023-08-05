/**
 * $Id: nccf_get_start_end_bound_indices.c 409 2011-01-19 18:06:34Z pletzer $
 */

void nccf_get_start_end_bound_indices(int ndims, const int dims[], 
					 const int normalVect[],
					 int exclusive,
					 int startIndices[],
					 int endIndices[]) {
  int i;
  for (i = 0; i < ndims; ++i) {
    /* by default, cover the entire domain */
    startIndices[i] = 0;
    endIndices[i] = dims[i] - 1 + exclusive;
    if (normalVect[i] > 0) {
      /* north, east, front, ... */
      startIndices[i] = dims[i] - 1;
    }
    else if (normalVect[i] < 0) {
      /* south, west, back, ... */
      endIndices[i] = 0 + exclusive;
    }
  }
}
