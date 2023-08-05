/**
 * $Id: nccf_inq_regrid_nnodes.c 742 2011-05-09 19:17:59Z edhartnett $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>

#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Get the number of nodes per cell
 *
 * \param regrid_id object Id
 * \param nnodes (output) number of nodes (2^ndims)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_inq_regrid_nnodes(int regrid_id, int *nnodes) {

    struct nccf_regrid_type *self;
    self = nccf_li_find(&CFLIST_REGRID, regrid_id);

    *nnodes = self->nnodes;

    return NC_NOERR;
}
