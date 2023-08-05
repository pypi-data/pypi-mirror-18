/**
 * $Id: nccf_inq_regrid_nvalid.c 742 2011-05-09 19:17:59Z edhartnett $
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>

#include <nccf_utility_functions.h>

/**
 * \ingroup gs_regrid_grp
 * Get the number of non-masked values in the domain
 *
 * \param regrid_id object Id
 * \param nvalid (output) number of non-masked values
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */
int 
nccf_inq_regrid_nvalid(int regrid_id, int *nvalid) {

    struct nccf_regrid_type *self;
    self = nccf_li_find(&CFLIST_REGRID, regrid_id);

    *nvalid = self->nvalid;

    return NC_NOERR;
}
