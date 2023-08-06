/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_free_coord.c 918 2012-02-07 22:10:36Z pletzer $
 * */

#include "nccf_coord.h"
#include <stdio.h>
#include <stdlib.h>

#include <netcdf.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_coord_grp
 * Free object (destructor).
 *
 * \param coordid coordinate ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_free_coord(int coordid) {

    struct nccf_coord_type *self;
    self = nccf_li_remove(&CFLIST_COORDINATE, coordid);
    if( nccf_li_get_nelem( &CFLIST_COORDINATE ) == 0 )
        nccf_li_del( &CFLIST_COORDINATE );

    /* free memory */
    if (self->coord_name) {
      free(self->coord_name);
      self->coord_name = NULL;
    }

    if (self->save) {
      free(self->data);
      self->data = NULL;
    }

    nccf_varDestroy(&self->coordVar);

    free(self);
    self = NULL;

    return NC_NOERR;
}
