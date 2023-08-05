/**
 * Read the global attributes from a file and populate a global attribute 
 * object.
 * $Id: nccf_def_global_from_file.c 869 2011-11-29 20:12:54Z pletzer $
 */

#include "nccf_global.h"
#include <netcdf.h>
#include <string.h>
#include "nccf_varObj.h"
#include "nccf_errors.h"

/**
 * \ingroup gs_global_grp
 * Define (construct) the global attributes from a netcdf file.
 *
 * \param filename Filename to retrieve the global attributes from
 * \param globalid (output) returned global ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_def_global_from_file(const char *filename, int *globalid){

  int totError = NC_NOERR, status = NC_NOERR;
  int ncid;

  /* Create the structure */
  struct nccf_global_type *self;
  self = (struct nccf_global_type *)
          malloc(sizeof( struct nccf_global_type));

  /* Initialize */
  self->global = NULL;

  /* Open file */
  status = nc_open(filename, NC_NOWRITE, &ncid);
  if( status ) return status;
  totError += abs(status);

  /* Get the global attributes */
  status = nccf_varCreateFromFile(&self->global, "", ncid, 1, 0);
  nc_close( ncid );

  /* Get the ID */
  if(CFLIST_GLOBAL == NULL) nccf_li_new(&CFLIST_GLOBAL);
  *globalid = nccf_li_add( &CFLIST_GLOBAL, self );

  return totError;

}
