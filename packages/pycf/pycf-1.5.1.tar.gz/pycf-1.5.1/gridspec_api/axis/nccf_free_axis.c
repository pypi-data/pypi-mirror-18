/*
 * $Id: nccf_free_axis.c 918 2012-02-07 22:10:36Z pletzer $
 * */

#include "nccf_axis.h"
#include <stdlib.h>

#include <netcdf.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_axis_grp
 * Free object (destructor).
 *
 * \param axisid coordinate ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer (Tech-X Corp.) and Ed Hartnett (UCAR).
 */
int nccf_free_axis(int axisid) {

    struct nccf_axis_type *self;
    self = nccf_li_remove(&CFLIST_AXIS, axisid);
    if( nccf_li_get_nelem( &CFLIST_AXIS ) == 0 )
        nccf_li_del( &CFLIST_AXIS );

    /* free memory */
    if (self->data) {
      free(self->data);
      self->data = NULL;
    }
    if (self->axis_name) {
      free(self->axis_name);
      self->axis_name = NULL;
    }
    nccf_varDestroy(&self->axisVar);
    free(self);
    self = NULL;

    return NC_NOERR;
}
