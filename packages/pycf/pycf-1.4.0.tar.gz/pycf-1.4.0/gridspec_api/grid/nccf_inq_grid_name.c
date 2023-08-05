/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_inq_grid_ndims.c 439 2011-01-22 22:05:36Z pletzer $
 * */

#include "nccf_grid.h"
#include <stdio.h>
#include <string.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_grid_grp
 * Fill in the grid name for a given grid ID.
 *
 * \param gridid grid object Id
 * \param gridname (output) name of grid, must be able to hold NC_MAX_NAME characters
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_grid_name(const int gridid, 
					   char *gridname ){

   struct nccf_struct_grid_type *self;

   self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

   strcpy( gridname, self->gridname );

   return NC_NOERR;
}
