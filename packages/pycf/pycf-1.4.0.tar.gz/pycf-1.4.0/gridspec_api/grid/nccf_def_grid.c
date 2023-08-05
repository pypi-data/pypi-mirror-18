/**
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_def_grid.c 942 2016-09-05 03:02:56Z pletzer $
 */

#include "nccf_errors.h"
#include <nccf_constants.h>
#include <nccf_utility_functions.h>
#include "nccf_grid.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <nccf_coord.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>

struct CFLISTITEM *CFLIST_STRUCTURED_GRID;

/** \defgroup gs_grid_grp Structured grids
    \ingroup gridspec_grp

Curvilinear, structured grids are collections of coordinates, one
for each spatial dimension. Grids keep a reference to the 
underlying coordinate objects. Therefore, coordinate objects must 
exist prior to the construction of a grid and coordinate objects
should not be freed before all operations on a structured grid have 
been completed.

*/

/**
 * \ingroup gs_grid_grp
 * Define structured grid (acts as a constructor).
 *
 * \param coordids coordinates IDs of the grid.
 * \param gridname name this grid will be given
 * \param gridid (output) grid ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_def_grid(const int coordids[], const char *gridname,
                         int *gridid){
 
    /* Instantiate object */
    struct nccf_struct_grid_type *self;
    self = (struct nccf_struct_grid_type *)
             malloc(sizeof(struct nccf_struct_grid_type));

    int i, ndims, status, ier = NC_NOERR;

    /* Initialization */
    self->coordids = NULL;
    self->ndims = 0;
    self->gridname = NULL;
    self->imask = NULL;
    self->coord_periodicity = NULL;

    /* Grid Name */
    self->gridname = (char*)calloc(STRING_SIZE, sizeof(char));
    strcpy(self->gridname, gridname);

    /* Get the number of dimensions from the first coordinate 
       must have at least one element */
    if (coordids) {
      status = nccf_inq_coord_ndims(coordids[0], &ndims);
      if (status != NC_NOERR) ier = NCCF_ENOCOORDID;
      self->ndims = ndims;

      self->coordids = (int *) malloc(ndims * sizeof( int ));
      for(i = 0; i < ndims; i++) {
        /* store the coordinate ids */
        self->coordids[i] = coordids[i];
      }

    }
    status = nccf_detect_grid_periodicity(self);

    /* Create a new, global list of grids, if need be */
    if(CFLIST_STRUCTURED_GRID == NULL) 
            nccf_li_new(&CFLIST_STRUCTURED_GRID);

    /* Add this instance to the linked list */
    *gridid  = nccf_li_add(&CFLIST_STRUCTURED_GRID, self);

    return ier;
}
