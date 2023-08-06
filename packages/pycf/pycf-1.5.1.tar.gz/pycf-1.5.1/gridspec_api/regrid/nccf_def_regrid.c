/**
 * $Id: nccf_def_regrid.c 856 2011-11-08 17:44:01Z pletzer $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>

#include <nccf_coord.h>
#include <nccf_grid.h>
#include <nccf_utility_functions.h>

struct CFLISTITEM *CFLIST_REGRID;

/*! \defgroup gs_regrid_grp Structured data regridding
  \ingroup gridspec_grp

Regridding is an interpolation operation, which takes the data attached
to an original grid and computes corresponding values on a target grid. The 
regridding operation assumes that both grids are structured 
and involves linear interpolation, i.e. only the closest neighbor 
values are used to determine the interpolated values. The interpolated
values are guaranteed to be within the range of neighboring values. 

Interpolation requires the location of a target position in index space. 
A pseudo-Newton scheme is used to find the index position. A single iteration
is sufficient in the case of a uniform grid, more iterations are required 
when the grid is locally refined and/or highly warped. 

Regridding only applies to target positions that have been found to lie
within the original grid. Regridding is a no-operation for those target 
positions that lie outside the original grid, or for target positions which 
could not be determined to lie within the original grid.  It is not
an error to have non-overlapping original and target grids. 

When regridding it is possible to exclude some regions (e.g. land in 
an ocean model) and this is achieved by adding forbidden boxes to the
regridding object. Care should also be taken when the original grid has a 
cut in coordinate space, that is a discontinuity in coordinates. This case
 arises when the longitudes jump by 360 degrees in particular. To remove the 
possibility for the interpolation algorithm to erroneously find the target 
position to lie within the cut (multi-valued coordinates are not allowed), 
it is advisable to add a forbidden box at the cut location.

*/

/**
 * \ingroup gs_regrid_grp
 * Define a regridding object (acts as a constructor).
 *
 * \param ori_grid_id original grid id.
 * \param tgt_grid_id target grid id.
 * \param regrid_id (output) grid ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_regrid(int ori_grid_id, int tgt_grid_id, int *regrid_id) {

  int totErr = NC_NOERR;
  int status;

  /* Instantiate object */
  struct nccf_regrid_type *self;
  self = (struct nccf_regrid_type *)
    malloc(sizeof(struct nccf_regrid_type));

  /* Initialize */
  self->ndims = 0;
  self->ntargets = 0;
  self->nvalid = 0;
  nccf_li_new(&self->box_lohi);
  self->ori_grid_id = ori_grid_id;
  self->tgt_grid_id = tgt_grid_id;

  /* Initialize the weights, index and inside_domain structures */
  nccf_varCreate(&self->weights_stt, "weights");
  nccf_varSetAttribText(&self->weights_stt, CF_ATTNAME_CF_TYPE_NAME, 
                        CF_REGRID_WEIGHTS);

  nccf_varCreate(&self->lower_corner_indices_stt, "indices");
  nccf_varSetAttribText(&self->lower_corner_indices_stt, 
                        CF_ATTNAME_CF_TYPE_NAME, 
                        CF_REGRID_INDICES);

  nccf_varCreate(&self->inside_domain_stt, "inside_domain");
  nccf_varSetAttribText(&self->inside_domain_stt, CF_ATTNAME_CF_TYPE_NAME, 
                        CF_REGRID_INSIDE_DOMAIN);

  /* Get number of space dimensions */
  status = nccf_inq_grid_ndims(ori_grid_id, &self->ndims);
  totErr += abs(status);

  
  /* Add the objet to the list */
  if (CFLIST_REGRID == NULL) nccf_li_new(&CFLIST_REGRID);
  *regrid_id = nccf_li_add(&CFLIST_REGRID, self);

  return totErr;
}
