/*
 * $Id: nccf_def_coord_from_file.c 895 2011-12-22 13:12:38Z pletzer $
 *
 */

#include "nccf_coord.h"
#include <netcdf.h>
#include <string.h>
#include <stdlib.h>
#include "nccf_varObj.h"

/**
 * \ingroup gs_coord_grp
 * Define (construct) a coordinate object from a netcdf file.
 *
 * \param filename name of the netcdf file
 * \param coord_name name of coordinate in file
 * \param coordid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 * \note the coordinate data will be cast into doubles, regardless
 * of what the stored data type is.
 */
int nccf_def_coord_from_file(const char *filename,
              const char *coord_name,
              int *coordid){

  int totError = NC_NOERR;
  int ncid, status = NC_NOERR;
  const int read_data = 1;
  const int cast_as_doubles = 1;
  struct nccf_coord_type *self;
  self = (struct nccf_coord_type *)
    malloc(sizeof(struct nccf_coord_type));
  
  // read the variable
  status = nc_open(filename, NC_NOWRITE, &ncid);
  if (status) return status;
  totError += abs(status);

  // note: data will be cast as doubles
  nccf_varCreateFromFile(&self->coordVar, coord_name, ncid, 
                         read_data, cast_as_doubles);
  status = nc_close(ncid);
  totError += abs(status);

  /* add an element to the linked list */
  if (CFLIST_COORDINATE == NULL) nccf_li_new(&CFLIST_COORDINATE);

  *coordid = nccf_li_add(&CFLIST_COORDINATE, self);

  // this will be removed
  self->coord_name = strdup(coord_name);
  nccf_varGetDataPtr(&self->coordVar, (void **)&self->data);
  self->save = 0;

  return totError;
}
