/**
 * $Id: nccf_def_mosaic_from_file.c 920 2012-03-20 23:11:28Z dkindig $
 */

#include "nccf_mosaic.h"
#include <netcdf.h>
#include "nccf_varObj.h"

// std includes
#include <string.h>
#include <stdio.h>


/* Local functions - Ultimitely get stored in the mosaic structure where 
 * external functions can read them */
int nccf_inq_mosaic_ndims_from_file(int ncid, int *ndims) {
  struct nccf_var_obj *v;
  int *dims;
  nccf_varCreateFromFile(&v, CF_MOSAIC_COORDINATE_NAME, ncid, 1, 0);
  nccf_varGetDimsPtr(&v, &dims);
  *ndims = dims[0];
  nccf_varDestroy(&v);
  return NC_NOERR;
}

int nccf_inq_mosaic_ncontacts_from_file(int ncid, int *ncontacts) {
  struct nccf_var_obj *v;
  int *dims;
  nccf_varCreateFromFile(&v, CF_MOSAIC_TILE_CONTACTS, ncid, 1, 0);
  nccf_varGetDimsPtr(&v, &dims);
  *ncontacts = dims[0];
  nccf_varDestroy(&v);
  return NC_NOERR;
}

int nccf_inq_mosaic_ngrids_from_file(int ncid, int *ngrids) {
  struct nccf_var_obj *v;
  int *dims;
  nccf_varCreateFromFile(&v, CF_MOSAIC_TILE_NAMES, ncid, 1, 0);
  nccf_varGetDimsPtr(&v, &dims);
  *ngrids = dims[0];
  nccf_varDestroy(&v);
  return NC_NOERR;
}

/**
 * \ingroup gs_mosaic_grp
 * Define (construct) a mosaic from a netcdf file.
 *
 * \param filename file name
 * \param name name of the mosaic
 * \param mosaicid (output) ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_def_mosaic_from_file(const char *filename, const char *name,
				int *mosaicid) {

  int ncid, status = NC_NOERR, i;
  int totError = NC_NOERR;
  char *coordname;
  
  struct nccf_mosaic_type *self;
  self = (struct nccf_mosaic_type *)
    malloc(sizeof(struct nccf_mosaic_type));
  
  self->name = ( char* )calloc( STRING_SIZE, sizeof( char ));
  strcpy(self->name, name);

  // open file
  status = nc_open(filename, NC_NOWRITE, &ncid);
  if( status ) return status;
  totError += abs(status);

  // Initialize the mosaic structure
  self->coordnameslist   = NULL;
  self->gridnameslist    = NULL;
  self->gridtogridlist   = NULL;
  self->contactindexlist = NULL;
  nccf_li_new(&self->coordnameslist);
  nccf_li_new(&self->gridnameslist);
  nccf_li_new(&self->gridtogridlist);
  nccf_li_new(&self->contactindexlist);
  self->ncontacts = 0;
  self->ngrids    = 0;
  self->gridids   = NULL;
  self->ndims     = 0;
  self->gs_slice_format = NULL;

  // Read the information from the file
  status = nccf_varCreateFromFile(&self->coordnames, CF_MOSAIC_COORDINATE_NAME, 
				  ncid, 1, 0);
  totError += abs(status);
  status = nccf_varCreateFromFile(&self->gridNames, CF_MOSAIC_TILE_NAMES, 
				  ncid, 1, 0);
  totError += abs(status);
  status = nccf_varCreateFromFile(&self->gridToGrid, CF_MOSAIC_TILE_CONTACTS, 
				  ncid, 1, 0);
  totError += abs(status);
  status = nccf_varCreateFromFile(&self->contactIndex, CF_MOSAIC_CONTACT_MAP, 
				  ncid, 1, 0);
  totError += abs(status);

  status = nccf_inq_mosaic_ndims_from_file(ncid, &self->ndims);
  totError += abs(status);

  status = nccf_inq_mosaic_ngrids_from_file(ncid, &self->ngrids);
  totError += abs(status);

  status = nccf_inq_mosaic_ncontacts_from_file(ncid, &self->ncontacts);
  totError += abs(status);

  // get pointer to the grid file name list
  char *gridNamesStr;
  nccf_varGetDataPtr(&self->gridNames, (void **) &gridNamesStr);
  int *gridNamesDims;
  nccf_varGetDimsPtr(&self->gridNames, &gridNamesDims);

  // get pointer to the coordinate name list
  char *coordnamesStr;
  nccf_varGetDataPtr(&self->coordnames, (void **) &coordnamesStr);
  int *coordnamesDims;
  nccf_varGetDimsPtr(&self->coordnames, &coordnamesDims);
  int strLengthCoordNames = coordnamesDims[1];

  // build a list of strings for the coordinate names
  for (i = 0; i < self->ndims; ++i) {
    coordname = (char *) calloc( strLengthCoordNames, sizeof(char) );
    strcpy( coordname, &coordnamesStr[ i * strLengthCoordNames ] );
    nccf_li_add( &self->coordnameslist, coordname );
  }

  // load gridids with NULL for later.
  self->gridids = NULL;
  
  // close the file
  status = nc_close(ncid);
  totError += abs(status);

  // add object to global list of mosaics
  if (CFLIST_MOSAIC == NULL) nccf_li_new(&CFLIST_MOSAIC);
  *mosaicid = nccf_li_add( &CFLIST_MOSAIC, self );

  return totError;
}
