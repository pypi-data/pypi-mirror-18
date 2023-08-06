/*
 * API to define a structured grid for the gridspec convention to libcf.
 *
 * $Id: nccf_put_regrid.c 856 2011-11-08 17:44:01Z pletzer $
 */

#include <nccf_regrid.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netcdf.h>
#include <libcf_src.h>
#include <nccf_grid.h>
#include <nccf_coord.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_regrid_grp
 * Write regrid weights, indices and domain location to a file
 *
 * \param regrid_id regrid ID created by nccf_def_regrid
 * \param ncid netcdf file id
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer, Dave Kindig, Tech-X Corp.
 */
int nccf_put_regrid(int regrid_id, int ncid){

  int status = NC_NOERR;
  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  if(( status = nccf_varSetAttribInt( &self->inside_domain_stt, 
                                      "nvalid", self->nvalid )));

  status = nccf_writeListOfVars(ncid, 3, self->weights_stt,
                                         self->lower_corner_indices_stt,
                                         self->inside_domain_stt);

  return status;
}
