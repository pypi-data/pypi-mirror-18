/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_inq_grid_coordnames.c 981 2016-09-14 08:23:44Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Fill in coordinate names.
 *
 * \param gridid grid object Id
 * \param coordnames (output) list of coordinate object names, each name must be able to hold NC_MAX_NAME characters
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_grid_coordnames(const int gridid, 
					                   char **coordnames ){

   int i;
   struct nccf_struct_grid_type *self;

   self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

   for (i = 0; i < self->ndims; ++i) {
     nccf_inq_coord_name(self->coordids[i], coordnames[i]);
   }

   return NC_NOERR;
}
