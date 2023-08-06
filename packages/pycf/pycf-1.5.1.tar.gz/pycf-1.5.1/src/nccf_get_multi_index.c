/**
 * $Id: nccf_get_multi_index.c 373 2011-01-14 19:53:49Z pletzer $
 */

void nccf_get_multi_index(int ndims, const int dims[], int index, int inx[]) {
  int i;
  /* prodDims would be (n1*n2, n2, 1) for dims == (n0, n1, n2) */
  int prodDims[ndims];
  prodDims[ndims - 1] = 1;
  for (i = ndims - 2; i >= 0; --i) {
    prodDims[i] = prodDims[i + 1] * dims[i + 1];
  }
  for (i = 0; i < ndims; ++i) {
    inx[i] = index / prodDims[i] % dims[i];
  }
}
