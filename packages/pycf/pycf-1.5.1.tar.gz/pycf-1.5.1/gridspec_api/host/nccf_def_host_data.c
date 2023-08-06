/* $Id: nccf_def_host_data.c 822 2011-09-13 14:39:33Z pletzer $ */

#include <nccf_host.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include <nccf_errors.h>
#include <nccf_global.h>
#include <nccf_axis.h>
#include <nccf_coord.h>
#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_constants.h>

/**
 * \ingroup gs_host_grp
 * Define the data attached to a grid tile
 * 
 * \param hostid the ID for the host object
 * \param varname the variable name
 * \param gfindx the index of the tile
 * \param read_data set to 0 if data should not be read from disk
 * \param dataid the ID of the variable (output)
 * \return NC_NOERR on success
 * \author Alexander Pletzer and Dave Kindig, Tech-X Corp
 * \note This is a constuctor call for the data, the underlying
 *       grid, and the coordinate objects. Users are expected
 *       to release the memory of the data object, the grid, and
 *       the coordinates
 */
int nccf_def_host_data(int hostid, const char *varname, int gfindx, 
		       int read_data, int *dataid) {

  int toterr = 0;
  int status;
  *dataid = -1;
  
  int ngrids;
  status = nccf_inq_host_ngrids(hostid, &ngrids);
  toterr += abs(status);
  if (gfindx >= ngrids) {
    return NCCF_EBADGRIDINDEX;
  }

  /* Get the variable file index, the variable can be static
     or time dependent */
  int vfindx = -1;
  char fdataname[STRING_SIZE]; fdataname[0] = '\0';
  status = nccf_inq_host_statfileindex(hostid, varname, 
				       &vfindx);
  if (status == NC_NOERR && vfindx >= 0) {
    // fetch the file name of the static variable
    status = nccf_inq_host_statfilename(hostid, vfindx, 
					gfindx, fdataname);
  }
  else {
    // try time dependent file since varname appears
    // not to be a static file
    status = nccf_inq_host_timefileindex(hostid, varname, 
					 &vfindx);
    toterr += abs(status);
    if (status == NC_NOERR && vfindx >= 0) {
      int tfindx = 0;
      status = nccf_inq_host_timefilename(hostid, tfindx, vfindx, 
					  gfindx, fdataname);
      toterr += abs(status);
    }
  }
  if (fdataname[0] == '\0' || vfindx < 0 || status != 0) {
    // varname does not appear to exist
    return NCCF_EBADVAR;
  }

  /* Read the mosaic file name and build the mosaic */
  char fname[STRING_SIZE]; fname[0] = '\0';
  status = nccf_inq_host_mosaicfilename(hostid, fname);
  toterr += abs(status);
  // set mosaic name to mosaic file name minus suffix
  char mname[STRING_SIZE]; mname[0] = '\0';
  int i = 0;
  while (i < STRING_SIZE-1 && fname[i] != '.') {
    mname[i] = fname[i];
    i++;
  }
  mname[i] = '\0';
  int mosaicid;
  status = nccf_def_mosaic_from_file(fname, mname, &mosaicid);
  toterr += abs(status);
  int ndims;
  status = nccf_inq_mosaic_ndims(mosaicid, &ndims);
  toterr += abs(status);
  if (ndims <= 0) {
    status = nccf_free_mosaic(mosaicid);
    return NCCF_ENDIMS;
  }
  char **coordnames;
  coordnames = malloc(ndims * sizeof(char *));
  for (i = 0; i < ndims; ++i) {
    coordnames[i] = calloc(STRING_SIZE, sizeof(char));
  }
  status = nccf_inq_mosaic_coordnames(mosaicid, coordnames);
  toterr += abs(status);

  /* Read the coordinates and build the coordinate objects, both
     cooridnates are assumed to be in the same file */
  status = nccf_inq_host_gridfilename(hostid, gfindx, fname);
  int coordids[ndims];
  for (i = 0; i < ndims; ++i) {
    status = nccf_def_coord_from_file (fname, coordnames[i], &coordids[i]);
  }

  /* Build the grid object */
  int gridid;
  char *gridname = calloc(STRING_SIZE, sizeof(char));
  status = nccf_inq_mosaic_gridname(mosaicid, gfindx, gridname);
  status = nccf_def_grid(coordids, gridname, &gridid);

  /* Build the data object */
  status = nccf_def_data_from_file(fdataname, gridid, 
				   varname, read_data, 
				   dataid);

  /* Clean up */
  free(gridname);
  for (i = 0; i < ndims; ++i) {
    free(coordnames[i]);
  }
  free(coordnames);
  status = nccf_free_mosaic(mosaicid);

  return toterr;
}
