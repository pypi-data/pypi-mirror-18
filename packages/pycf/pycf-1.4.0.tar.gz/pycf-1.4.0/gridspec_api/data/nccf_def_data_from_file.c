/**
 * $Id: nccf_def_data_from_file.c 1012 2016-10-11 19:22:04Z pletzer $
 */

#include <nccf_data.h>
#include <stdio.h>
#include <string.h>
#include <nccf_grid.h>
#include <nccf_coord.h>

/**
 * \ingroup gs_data_grp
 * Define data object from netcdf file (constructor).
 *
 * \param filename name of the netcdf file
 * \param gridid Id of the grid object associated with the data
 * \param varname variable name of the data object stored in file
 * \param read_data set to 1 if data should be read, 0 otherwise
 * \param dataid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_data_from_file(const char *filename,
                            int gridid, const char *varname,
                            int read_data, int *dataid) {

  int status;
  int totError = 0;
  int ncid;
  const char *coordinates;
  float *data;

  /* Open the file read the structure */
  status = nc_open(filename, NC_CLOBBER, &ncid );
  if (status != NC_NOERR) return status;

  /* Create the object */
  struct nccf_data_type *self;
  self = (struct nccf_data_type *)
    malloc(sizeof(struct nccf_data_type));

  /* Default initialization */
  self->save = 0;
  self->data = NULL;
  self->gridid = gridid;

  /* Fill in members */
  self->name = (char*) calloc(STRING_SIZE, sizeof(char));
  sprintf(self->name, "%s", varname);

  /* Create the data object for the given variable */
  const int keep_type = 0;
  status = nccf_varCreateFromFile(&self->dataVar, varname, ncid, 
                                  read_data, keep_type);
  totError += abs(status);

  /* Get data size information */
  nccf_varGetNumDims( &self->dataVar, &self->ndims );

  /* Get the data */
  status = nccf_varGetDataPtr( &self->dataVar,( void **) &data );
  totError += abs(status);

  /* Find the coordinate object associated with the above data */
  status = nccf_varGetAttribPtr(&self->dataVar, CF_COORDINATES, 
		                            (const void **) &coordinates);
  totError += abs(status);

  if ((status = nc_close(ncid))) ERR;

  /* Add the objet to the list */
  if (CFLIST_STRUCTURED_DATA == NULL) nccf_li_new(&CFLIST_STRUCTURED_DATA);
  *dataid = nccf_li_add(&CFLIST_STRUCTURED_DATA, self);

  return totError;
}
