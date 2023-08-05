/**
 * $Id: nccf_inq_regrid_weights.c 921 2012-03-22 01:44:24Z dkindig $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>
#include <stdio.h>

#include <nccf_coord.h>
#include <nccf_grid.h>
#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Get the weights, should be called after nccf_compute_regrid_weights.
 *
 * \param regrid_id object Id
 * \param tgt_indices index set of the target point, dimensioned ndims
 * \param ori_nodes flat indices on the original grid, should be dimensioned
 *                  2^ndims (output)
 * \param weights interpolation weights for the above flat indices, should be
                  dimensioned 2^ndims (output)
 * \return NC_NOERR on success
 *
 * \see nccf_compute_regrid_weights
 *
 * \note the sum of the weights may be < 1 if some weights fall outside
 *       the domain
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_inq_regrid_weights(int regrid_id, const int tgt_indices[],
                        int ori_nodes[], double weights[]) {
  
  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  int totErr = NC_NOERR;
  int status;

  int i, j, ibig, k, k2;

  double *allweights;
  status = nccf_varGetDataPtr(&self->weights_stt, 
                              (void **)&allweights);
  totErr += abs(status);

  int *lower_corner_indices;
  status = nccf_varGetDataPtr(&self->lower_corner_indices_stt, 
                              (void **)&lower_corner_indices);
  totErr += abs(status);

  const int *displ;
  status = nccf_varGetAttribPtr(&self->lower_corner_indices_stt,
                                CF_INDEX_OFFSETS, 
                                (const void **)&displ);
  totErr += abs(status);

  const int *ori_dims;
  status = nccf_varGetAttribPtr(&self->lower_corner_indices_stt,
                                CF_ORI_DIMS, 
                                (const void **)&ori_dims);
  totErr += abs(status);
  
  char *inside_domain;
  status = nccf_varGetDataPtr(&self->inside_domain_stt, 
                            (void **)&inside_domain);
  totErr += abs(status);

  int nNodes = 1;
  int ori_ntot = 1;
  for (i = 0; i < self->ndims; ++i) {
    nNodes *= 2;
    ori_ntot *= ori_dims[i];
  }

  int tgt_coordids[self->ndims];
  status = nccf_inq_grid_coordids(self->tgt_grid_id, tgt_coordids);
  totErr += abs(status);

  int tgt_dims[self->ndims];
  status = nccf_inq_coord_dims(tgt_coordids[0], tgt_dims);
  totErr += abs(status);

  /* compute the flat index */
  ibig = nccf_get_flat_index(self->ndims, tgt_dims, tgt_indices);

  for (j = 0; j < nNodes; ++j) {
    k2 = lower_corner_indices[ibig] + displ[j];
    /* adjust if falling out of domain */
    k2 = (k2 > ori_ntot - 1? lower_corner_indices[ibig]: k2);
    ori_nodes[j] = k2;
    k = ibig*nNodes + j;
    /* weight is zero if outside domain */
    weights[j] = allweights[k] * inside_domain[ibig];
  }

  return totErr;
}
