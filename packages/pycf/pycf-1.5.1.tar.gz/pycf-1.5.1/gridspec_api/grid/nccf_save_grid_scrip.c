/* $Id: nccf_save_grid_scrip.c 738 2011-05-06 22:26:09Z edhartnett $ */

#include <nccf_grid.h>
#include <math.h>
#include <netcdf.h>
#include <nccf_coord.h>

/**
 * \ingroup gs_grid_grp
 * Save grid object in SCRIP compatible file
 *
 * \param gridid grid object Id
 * \param filename NetCDF file name
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_save_grid_scrip(int gridid, const char *filename) {
  int ncid;
  int ierr;
  int tot_err = NC_NOERR;
  int ilon = -1, ilat = -1;
  int i, j, k;
  int yesno;
  int ncells;
  char lon_units[STRING_SIZE];
  char lat_units[STRING_SIZE];

  struct nccf_struct_grid_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_GRID, gridid);

  if (self->ndims != 2) {
    // no op if not a lon-lat grid
    return NC_NOERR;
  }
			
  // locate the lon-lat coordinates
  for (i = 0; i < self->ndims; ++i) {
    ierr = nccf_is_coord_lon(self->coordids[i], &yesno);
    tot_err += abs(ierr);
    if (yesno == 1) {
      ilon = i;
      ierr = nccf_inq_coord_units(self->coordids[i], lon_units);
      tot_err += abs(ierr);
    }
    ierr = nccf_is_coord_lat(self->coordids[i], &yesno);
    tot_err += abs(ierr);
    if (yesno == 1) {
      ilat = i;
      ierr = nccf_inq_coord_units(self->coordids[i], lat_units);
      tot_err += abs(ierr);
    }
  }

  // number of cells
  int dims[self->ndims];
  int dims_cell[self->ndims];
  ierr = nccf_inq_coord_dims(self->coordids[0], dims);
  tot_err += abs(ierr);
  ncells = 1;
  for (i = 0; i < self->ndims; ++i) {
    dims_cell[i] = dims[i] - 1;
    ncells *= dims_cell[i];
  }
  int ncorners = 2*2;

  // save to netcdf file
  ierr = nc_create(filename, NC_CLOBBER, &ncid);
  tot_err += abs(ierr);

  // create var objects
  struct nccf_var_obj *grid_dims;
  struct nccf_var_obj *grid_center_lon;
  struct nccf_var_obj *grid_center_lat;
  struct nccf_var_obj *grid_imask;
  struct nccf_var_obj *grid_corner_lon;
  struct nccf_var_obj *grid_corner_lat;
  struct nccf_var_obj *global;

  const char *dims_cell_names[] = {"grid_rank"};
  const char *dims_center_names[] = {"grid_size"};
  const char *dims_corner_names[] = {"grid_size", "grid_corners"};

  const int dims_cells[] = {self->ndims};
  const int dims_center[] = {ncells};
  const int dims_corner[] = {ncells, pow(2, self->ndims) };

  ierr = nccf_varCreate(&grid_dims, "grid_dims");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_dims, 1, dims_cells, dims_cell_names);
  tot_err += abs(ierr);

  ierr = nccf_varCreate(&grid_center_lon, "grid_center_lon");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_center_lon, 1, dims_center, dims_center_names);
  tot_err += abs(ierr);
  ierr = nccf_varSetAttribText(&grid_center_lon, "units", lon_units);
  tot_err += abs(ierr);

  ierr = nccf_varCreate(&grid_center_lat, "grid_center_lat");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_center_lat, 1, dims_center, dims_center_names);
  tot_err += abs(ierr);
  ierr = nccf_varSetAttribText(&grid_center_lat, "units", lat_units);
  tot_err += abs(ierr);

  ierr = nccf_varCreate(&grid_imask, "grid_imask");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_imask, 1, dims_center, dims_center_names);
  tot_err += abs(ierr);

  ierr = nccf_varCreate(&grid_corner_lon, "grid_corner_lon");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_corner_lon, 2, dims_corner, dims_corner_names);
  tot_err += abs(ierr);
  ierr = nccf_varSetAttribText(&grid_corner_lon, "units", lon_units);
  tot_err += abs(ierr);

  ierr = nccf_varCreate(&grid_corner_lat, "grid_corner_lat");
  tot_err += abs(ierr);
  ierr = nccf_varSetDims(&grid_corner_lat, 2, dims_corner, dims_corner_names);
  tot_err += abs(ierr);
  ierr = nccf_varSetAttribText(&grid_corner_lat, "units", lat_units);
  tot_err += abs(ierr);

  // set the data
  ierr = nccf_varSetDataPtr(&grid_dims, NC_INT, dims_cell); // should really be NC_LONG
  tot_err += abs(ierr);

  double *lons;
  double *lats;
  ierr = nccf_get_coord_data_pointer(self->coordids[ilon], &lons);
  tot_err += abs(ierr);
  ierr = nccf_get_coord_data_pointer(self->coordids[ilat], &lats);
  tot_err += abs(ierr);
  double *center_lon = (double *) malloc(sizeof(double) * ncells);
  double *center_lat = (double *) malloc(sizeof(double) * ncells);
  int *imask = (int *) malloc(sizeof(int) * ncells);
  double *corner_lon = (double *) malloc(sizeof(double) * ncorners * ncells);
  double *corner_lat = (double *) malloc(sizeof(double) * ncorners * ncells);
  k = 0;
  for (i = 0; i < dims[0]-1; ++i){
    for (j = 0; j < dims[1]-1; ++j) {

      center_lon[k]  = lons[(j+0) + (i+0)*dims[0]];
      center_lon[k] += lons[(j+1) + (i+0)*dims[0]];
      center_lon[k] += lons[(j+0) + (i+1)*dims[0]];
      center_lon[k] += lons[(j+1) + (i+1)*dims[0]];
      center_lon[k] /= 4.0;

      center_lat[k]  = lats[(j+0) + (i+0)*dims[0]];
      center_lat[k] += lats[(j+1) + (i+0)*dims[0]];
      center_lat[k] += lats[(j+0) + (i+1)*dims[0]];
      center_lat[k] += lats[(j+1) + (i+1)*dims[0]];
      center_lat[k] /= 4.0;

      imask[k] = 1;
      if (self->imask) {
	if ( (self->imask[(j+0) + (i+0)*dims[0]] == 0) ||
	     (self->imask[(j+1) + (i+0)*dims[0]] == 0) ||
	     (self->imask[(j+0) + (i+1)*dims[0]] == 0) ||
	     (self->imask[(j+1) + (i+1)*dims[0]] == 0) ) {
	  imask[k] = 0;
	}
      }

      corner_lon[4*k + 0] = lons[(j+0) + (i+0)*dims[0]];
      corner_lon[4*k + 1] = lons[(j+1) + (i+0)*dims[0]];
      corner_lon[4*k + 2] = lons[(j+1) + (i+1)*dims[0]];
      corner_lon[4*k + 3] = lons[(j+0) + (i+1)*dims[0]];

      corner_lat[4*k + 0] = lats[(j+0) + (i+0)*dims[0]];
      corner_lat[4*k + 1] = lats[(j+1) + (i+0)*dims[0]];
      corner_lat[4*k + 2] = lats[(j+1) + (i+1)*dims[0]];
      corner_lat[4*k + 3] = lats[(j+0) + (i+1)*dims[0]];

      k++;
    }
  }
  
  ierr = nccf_varSetDataPtr(&grid_center_lon, NC_DOUBLE, center_lon);
  tot_err += abs(ierr);
  ierr = nccf_varSetDataPtr(&grid_center_lat, NC_DOUBLE, center_lat);
  tot_err += abs(ierr);
  ierr = nccf_varSetDataPtr(&grid_imask, NC_INT, imask);
  tot_err += abs(ierr);
  ierr = nccf_varSetDataPtr(&grid_corner_lon, NC_DOUBLE, corner_lon);
  tot_err += abs(ierr);
  ierr = nccf_varSetDataPtr(&grid_corner_lat, NC_DOUBLE, corner_lat);
  tot_err += abs(ierr);

  // global attribute
  ierr = nccf_varCreate(&global, "");
  tot_err += abs(ierr);
  ierr = nccf_varSetAttribText(&global, "title", 
                               "libCF nccf_save_grid_scrip");

  // write the data
  ierr = nccf_writeListOfVars(ncid, 7, grid_dims, 
                              grid_center_lon, grid_center_lat, grid_imask,
                              grid_corner_lon, grid_corner_lat, global);
  tot_err += abs(ierr);

  // close file
  ierr = nc_close(ncid);
  tot_err += abs(ierr);

  // clean up
  free(corner_lon);
  free(corner_lat);
  free(imask);
  free(center_lon);
  free(center_lat);
  ierr = nccf_varDestroy(&grid_dims);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&grid_center_lon);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&grid_center_lat);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&grid_imask);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&grid_corner_lon);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&grid_corner_lat);
  tot_err += abs(ierr);
  ierr = nccf_varDestroy(&global);
  tot_err += abs(ierr);

  return tot_err;
}

