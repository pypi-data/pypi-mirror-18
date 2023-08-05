/**
 * $Id: nccf_def_regrid_from_file.c 869 2011-11-29 20:12:54Z pletzer $
 */

#include <nccf_regrid.h>
#include <netcdf.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <nccf_varObj.h>
#include <nccf_coord.h>
#include <nccf_grid.h>

int nccf_get_weights( int regrid_id, double **weights ){
  
  double **data;
  struct nccf_var_obj *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  nccf_varGetDataPtr( &self, ( void** ) &data );

  return NC_NOERR;

}

/**
 * \ingroup gs_regrid_grp
 * Create a regrid object from a file
 * 
 * /param filename File to read from
 * /param ndims Dimensions of grid
 * /param regrid_id regrid object to write
 * /return NC_NOERR on success
 *
 * \author Alexander Pletzer, Dave Kindig, Tech-X Corp.
 */
int nccf_def_regrid_from_file(const char *filename,
                   int *regridId) {

  int ncid;
  int status = NC_NOERR;
  int *dims;

  struct nccf_regrid_type *self;
  self = ( struct nccf_regrid_type* )malloc( sizeof( struct nccf_regrid_type ));

  /* initialize self */
  nccf_li_new( &self->box_lohi );

  self->nvalid = 0;
  const int *nvalid = NULL;

  status = nc_open( filename, NC_NOWRITE, &ncid );
  if( status ) return status;

  const int read_data = 1;
  const int as_double = 1;
  const int keep_type = 0;
  nccf_varCreateFromFile( &self->weights_stt, "weights", 
                          ncid, read_data, as_double );
  nccf_varCreateFromFile( &self->lower_corner_indices_stt, "indices", 
                          ncid, read_data, keep_type );
  nccf_varCreateFromFile( &self->inside_domain_stt, "inside_domain", 
                          ncid, read_data, keep_type );

  nccf_varGetDimsPtr( &self->weights_stt, &dims );
  self->ntargets = dims[0];
  self->nnodes = dims[1];

  self->ndims = 0;
  while ( powf(2.0f, (float) self->ndims) < (float)(self->nnodes) ) {
    self->ndims++;
  }

  nccf_varGetAttribPtr( &self->inside_domain_stt, "nvalid", 
                        (const void **)&nvalid );
  self->nvalid = *nvalid;

  if (( status = nc_close( ncid ))) ERR;

  /* Add the objet to the list */
  if (CFLIST_REGRID == NULL) nccf_li_new(&CFLIST_REGRID);
  *regridId = nccf_li_add(&CFLIST_REGRID, self);

  return NC_NOERR;

}
