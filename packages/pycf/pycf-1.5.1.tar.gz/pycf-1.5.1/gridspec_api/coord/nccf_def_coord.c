/**
 * API to define a coordinate for the gridspec convention of libcf.
 *
 * $Id: nccf_def_coord.c 939 2016-09-05 00:24:18Z pletzer $
 */

#include "nccf_coord.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <nccf_handle_error.h>
#include <nccf_varObj.h>

struct CFLISTITEM *CFLIST_COORDINATE;

/** \defgroup gs_coord_grp Structured coordinates
    \ingroup gridspec_grp

Structured curvilinear coordinates are in-memory objects that associate 
a position to a set of indices. The positions can be irregular in space. 
However, indexing is assumed to be regular.

*/

/**
 * \ingroup gs_coord_grp
 * Define a generic, structured grid coordinate (constructor).
 *
 * \param ndims number of space dimensions
 * \param dims dimensions along each axis
 * \param dimnames user defined dimension names
 * \param data pointer to the data
 * \param save != 0 in order to copy-save the data
 * \param name name of coordinate (e.g. "lon")
 * \param standard_name CF standard_name (or NULL if empty)
 * \param units CF units (or NULL if empty)
 * \param coordid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note copy-save means this object makes a copy of the data, otherwise
 *       it will take the pointer and the caller is responsible for 
 *       releasing the data memory.
 */
int nccf_def_coord(int ndims, const int *dims, const char **dimnames,
         const double *data,  int save,
         const char *name, const char *standard_name, 
         const char *units, int *coordid){

  int i, nvertex;
  struct nccf_coord_type *self;
  self = (struct nccf_coord_type *)
    malloc(sizeof(struct nccf_coord_type));
  nc_type type = NC_DOUBLE;

  /* initialization */
  self->coord_name = (char *) calloc(STRING_SIZE, sizeof(char));
  sprintf(self->coord_name, "%s", name);

  /* fill in the tile information */
  nccf_varCreate(&self->coordVar, name);
  nccf_varSetDims(&self->coordVar, ndims, dims, (const char **)dimnames);
  if (standard_name != NULL) {
    nccf_varSetAttribText(&self->coordVar, CF_ATTNAME_STANDARD_NAME, 
			  standard_name);
  }
  if (units != NULL) {
    nccf_varSetAttribText(&self->coordVar, CF_ATTNAME_UNITS, units);
  }
  //nccf_varSetAttribText(&self->coordVar, CF_ATTNAME_BOUNDS, name); /* coordinates are assumed nodal */

  /* take a reference to the data, or copy */
  self->save = save;
  if (save) {
    /* number of vertices */
    nvertex = 1;
    for (i = 0; i < ndims; ++i) {
      nvertex *= dims[i];
    }
    self->data = (double *) malloc(nvertex * sizeof(double));
    for (i = 0; i < nvertex; ++i) {
      /* copy */
      self->data[i] = data[i];
    }
  }
  else {
    /* set pointer */
    self->data = (double *) data;
  }

  /* set the pointer */
  nccf_varSetDataPtr(&self->coordVar, type, self->data);

  /* add an element to the linked list */
  if (CFLIST_COORDINATE == NULL) nccf_li_new(&CFLIST_COORDINATE);

  *coordid = nccf_li_add(&CFLIST_COORDINATE, self);

  return NC_NOERR;
}

/**
 * \ingroup gs_coord_grp
 * Define a longitude, structured grid coordinate (constructor).
 *
 * \param ndims number of space dimensions
 * \param dims dimensions along each axis
 * \param dimnames user defined dimension names
 * \param data pointer to the data
 * \param save != 0 in order to copy-save the data
 * \param coordid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note copy-save means this object makes a copy of the data, otherwise
 *       it will take the pointer and the caller is responsible for 
 *       releasing the data memory.
 */
int nccf_def_lon_coord(int ndims, const int *dims, const char **dimnames,
             const double *data,  int save, int *coordid){

  return nccf_def_coord(ndims, dims, dimnames, data, save, 
              CF_COORD_LON_VARNAME, CF_COORD_LON_STNAME, CF_COORD_LON_UNITS, 
              coordid);
}

/**
 * \ingroup gs_coord_grp
 * Define a latitude,  structured grid coordinate (constructor).
 *
 * \param ndims number of space dimensions
 * \param dims dimensions along each axis
 * \param dimnames user defined dimension names
 * \param data pointer to the data
 * \param save != 0 in order to copy-save the data
 * \param coordid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note copy-save means this object makes a copy of the data, otherwise
 *       it will take the pointer and the caller is responsible for 
 *       releasing the data memory.
 */
int nccf_def_lat_coord(int ndims, const int *dims, const char **dimnames, 
             const double *data, int save, int *coordid){

  return nccf_def_coord(ndims, dims, dimnames, data, save, 
              CF_COORD_LAT_VARNAME, CF_COORD_LAT_STNAME, CF_COORD_LAT_UNITS, 
              coordid);
}
