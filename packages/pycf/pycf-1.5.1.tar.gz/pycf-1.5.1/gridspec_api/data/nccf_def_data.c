/**
 * $Id: nccf_def_data.c 842 2011-09-30 13:41:35Z pletzer $
 */

#include <nccf_data.h>
#include <nccf_coord.h>
#include <nccf_grid.h>
#include <string.h>
#include <stdio.h>

/*! \defgroup gs_data_grp Structured data
  \ingroup gridspec_grp

Each structured grid can have data attached. Data objects refer to grid
objects and are defined on a per tile basis.
*/

struct CFLISTITEM *CFLIST_STRUCTURED_DATA;

/**
 * \ingroup gs_data_grp
 * Define data object (constructor).
 *
 * \param gridid structured grid object Id
 * \param name name of data object
 * \param standard_name CF standard name attribute of the data (or NULL if no standard_name)
 * \param units CF units attribute of the data (or NULL if no units)
 * \param time_dimname name of time dimension (or NULL if time independent)
 * \param dataid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_data(int gridid,
      const char *name, const char *standard_name,
      const char *units, const char *time_dimname, int *dataid) {

  int totError = NC_NOERR;
  int status, i;
  const char *space = " ";
  char coordName[STRING_SIZE];

  /* Create the object */
  struct nccf_data_type *self;
  self = (struct nccf_data_type *)
    malloc(sizeof(struct nccf_data_type));

  /* Default initialization */
  self->gridid = gridid;
  self->dataType = NC_NAT;
  self->name = NULL;
  self->ndims = 0;
  self->dataVar = NULL;
  self->save = 0;
  self->numRecords = 0;
  self->data = NULL;

  /* Fill in members */
  self->name = (char*) calloc(STRING_SIZE, sizeof( char ));
  sprintf(self->name, "%s", name);

  /* Create and populate netcdf-like variable */
  nccf_varCreate(&self->dataVar, name);
  if (standard_name != NULL) {
    nccf_varSetAttribText(&self->dataVar, CF_ATTNAME_STANDARD_NAME, 
			  standard_name);
  }
  if (units != NULL) {
    nccf_varSetAttribText(&self->dataVar, CF_ATTNAME_UNITS, units);
  }

  /* Determine the list of coordinate names */
  status = nccf_inq_grid_ndims(gridid, &self->ndims);
  totError += abs(status);
  int coordIds[self->ndims];
  status = nccf_inq_grid_coordids(gridid, coordIds);
  totError += abs(status);
  char *coordNames = (char *) calloc(self->ndims * STRING_SIZE, sizeof(char));
  for (i = 0; i < self->ndims; ++i) {
    status = nccf_inq_coord_name(coordIds[i], coordName);
    totError += abs(status);
    strcat(coordNames, coordName);
    if (i < self->ndims - 1) strcat(coordNames, space);
  }
  nccf_varSetAttribText(&self->dataVar, CF_COORDINATES, coordNames);
  free(coordNames);

  /* Set the variable dimension names and sizes */
  int *dims;
  dims = malloc(self->ndims * sizeof(int));
  status = nccf_inq_coord_dims(coordIds[0], dims);
  totError += abs(status);

  char **dimNames;
  dimNames = (char **) malloc( self->ndims * sizeof(char *));
  for (i = 0; i < self->ndims; ++i) {
    dimNames[i] = (char *) calloc(STRING_SIZE, sizeof(char));
  }
  status = nccf_inq_coord_dimnames(coordIds[0], dimNames);
  totError += abs(status);

  if (!time_dimname || strcmp(time_dimname, "") == 0) {
    /* static data */
    nccf_varSetDims(&self->dataVar, self->ndims, dims, 
		    (const char **) dimNames);
  }
  else {
    /* add time axis */
    int ndimsTime = self->ndims + 1;
    int dimsTime[ndimsTime];
    char **dimNamesTime = malloc( ndimsTime * sizeof(char *));
    for (i = 0; i < ndimsTime; ++i) {
      dimNamesTime[i] = (char *) calloc(STRING_SIZE, sizeof(char));
    }

    dimsTime[0] = NC_UNLIMITED;
    strncpy(dimNamesTime[0], time_dimname, STRING_SIZE);
    for (i = 0; i < self->ndims; ++i) {
      dimsTime[i + 1] = dims[i];
      strncpy(dimNamesTime[i + 1], dimNames[i], STRING_SIZE);
    }
    nccf_varSetDims(&self->dataVar, ndimsTime, dimsTime, 
		    (const char **)dimNamesTime);

    for (i = 0; i < ndimsTime; ++i) {
      free( dimNamesTime[i] );
    }
    free(dimNamesTime);
  }


  for (i = 0; i < self->ndims; ++i) {
    free(dimNames[i]);
  }
  free(dimNames);
  free(dims);

  /* Add the objet to the list */
  if (CFLIST_STRUCTURED_DATA == NULL) nccf_li_new(&CFLIST_STRUCTURED_DATA);
  *dataid = nccf_li_add(&CFLIST_STRUCTURED_DATA, self);

  return NC_NOERR;			     
}
