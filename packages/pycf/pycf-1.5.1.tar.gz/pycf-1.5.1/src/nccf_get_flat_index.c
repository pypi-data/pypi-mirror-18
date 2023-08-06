/**
 * $Id: nccf_get_flat_index.c 373 2011-01-14 19:53:49Z pletzer $
 */

int nccf_get_flat_index(int ndims, const int dims[], const int inx[]) {
  int res = 0;
  int nProd = 1;
  int i;
  for (i = ndims - 1; i >= 0; --i) {
    res += nProd * inx[i];
    nProd *= dims[i];
  }
  return res;
}
