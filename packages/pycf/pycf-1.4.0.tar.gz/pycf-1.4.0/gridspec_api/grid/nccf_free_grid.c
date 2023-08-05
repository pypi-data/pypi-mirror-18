/*
 * API to free a structured grid object for the gridspec convention to
 * libcf.
 *
 * $Id: nccf_free_grid.c 918 2012-02-07 22:10:36Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Free structured grid object.
 *
 * \param gridid grid ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_free_grid(int gridid) {

    struct nccf_struct_grid_type *self;
    self = nccf_li_remove(&CFLIST_STRUCTURED_GRID, gridid);
    if( nccf_li_get_nelem( &CFLIST_STRUCTURED_GRID ) == 0 )
        nccf_li_del( &CFLIST_STRUCTURED_GRID );

    /* call free below */
    if(self->gridname){
     free(self->gridname);
     self->gridname = NULL;
    }
    if(self->coordids) {
      free(self->coordids);
      self->coordids = NULL;
    }

    if (self->imask) {
      free(self->imask);
      self->imask = NULL;
    }

    if (self->coord_periodicity) {
      free(self->coord_periodicity);
      self->coord_periodicity = NULL;
    }

    /* Destroy object */
    free(self);
    self = NULL;

    return NC_NOERR;
}
