/**
 * API define host file.
 *
 * "$Id: nccf_def_host.c 809 2011-09-12 19:45:48Z dkindig $"
 */

#include <nccf_host.h>
#include <string.h>
#include <stdio.h>
#include <netcdf.h>

struct CFLISTITEM *CFLIST_HOST;

/*! \defgroup gs_host_grp Host file
  \ingroup gridspec_grp

  All the files composing a mosaic a linked together in a ``host'' file where
grids files, data, and mosaic files are listed.

*/

/**
 * \ingroup gs_host_grp
 *  Define an empty host file (in memory).
 *
 * \param coordinates_id the unique identifier binding the coordinates together
 * \param data_id the unique identifier binding the data together
 * \param nTimeSlices Number of files for one grid and one time dependent variable.
 * \param hostid (output) the created ID for the host object
 * \return NC_NOERR on success
 * \note nTimeSlices is the number of time files.
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_host(const char *coordinates_id, 
		  const char *data_id, 
		  int nTimeSlices, int *hostid) {

  struct nccf_host_type *self;
  self = (struct nccf_host_type *)malloc(sizeof(struct nccf_host_type));

  /* initialize */
  self->hasMosaic = 0;
  self->nGrids = 0;
  self->nVars  = 0;
  self->nTimeDataFiles = 0;
  self->nStatDataFiles = 0;
  self->nTimeSlices = nTimeSlices;  // Refers to the number of time slice files

  self->gridFiles = NULL;
  self->gridNames = NULL;
  self->timeDataFiles = NULL;
  self->statDataFiles = NULL;
  self->variables     = NULL;

  self->mosaicFileBuffer = NULL;
  self->coordinates_id   = NULL;
  self->data_id          = NULL;

  /* create */
  nccf_li_new(&self->gridFiles);
  nccf_li_new(&self->gridNames);
  nccf_li_new(&self->timeDataFiles);
  nccf_li_new(&self->statDataFiles);
  nccf_li_new(&self->variables);

  /* populate _ids */
  self->coordinates_id = (char*)calloc( 36+1, sizeof(char));
  self->data_id        = (char*)calloc( 36+1, sizeof(char));
  strcpy( self->coordinates_id, coordinates_id);
  strcpy( self->data_id, data_id);
  
  /* add to global list of objects */
  if (CFLIST_HOST == NULL) nccf_li_new(&CFLIST_HOST);

  *hostid = nccf_li_add( &CFLIST_HOST, self );

  return NC_NOERR;
}
