/*
 * $Id: nccf_def_coord_from_axes.c 851 2011-11-08 14:37:20Z pletzer $
 */

#include <nccf_utility_functions.h>
#include <nccf_axis.h>
#include "nccf_coord.h"
#include <stdlib.h>
#include <string.h>

/**
 * \ingroup gs_coord_grp
 * Create a curvilinear coordinate from a set of axes
 * (constructor).
 *
 * \param ndims number of space dimensions
 * \param axisids array of axis IDs
 * \param index_pos the coordinate values will vary along index_pos
 *                  and be the same along any other index axis
 * \param name name of coordinate (e.g. "lon")
 * \param standard_name CF standard_name (or NULL if empty)
 * \param units CF units (or NULL if empty)
 * \param coordid (output) ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_def_coord_from_axes(int ndims, const int *axisids, 
                             int index_pos, const char *name, 
                             const char *standard_name, 
                             const char *units, int *coordid){

  int tot_error = 0;
  const int save = 1;
  int dims[ndims];
  char **dimnames;
  double *data;
  int i, j, ntot, status;
  int ijk[ndims];
  void *axis_data;
  nc_type axis_data_type;

  dimnames = malloc(ndims * sizeof(char *));
 
  // get the dimensions and the dimension names
  for (i = 0; i < ndims; ++i) {
    dimnames[i] = calloc(STRING_SIZE, sizeof(char));
    status = nccf_inq_axis_len(axisids[i], &dims[i]);
    tot_error += abs(status);
    // dimension name is same as axis name
    status = nccf_inq_axis_name(axisids[i], dimnames[i]);
    tot_error += abs(status);
  }

  // 
  // construct the coordinate data
  //

  ntot = 1;
  for (i = 0; i < ndims; ++i) {
    ntot *= dims[i];
  }

  data = malloc(ntot * sizeof(double));

  status = nccf_get_axis_datapointer(axisids[index_pos], &axis_data);
  status = nccf_inq_axis_datatype(axisids[index_pos], &axis_data_type);
  if (axis_data_type == NC_DOUBLE) {
    double *axis_data_double = (double *) axis_data;
    for (j = 0; j < ntot; ++j) {
      nccf_get_multi_index(ndims, dims, j, ijk);
      data[j] = axis_data_double[ijk[index_pos]];
    }
  }
  else if (axis_data_type == NC_FLOAT) {
    float *axis_data_float = (float *) axis_data;
    for (j = 0; j < ntot; ++j) {
      nccf_get_multi_index(ndims, dims, j, ijk);
      data[j] = axis_data_float[ijk[index_pos]];
    }
  }
  else if (axis_data_type == NC_INT) {
    int *axis_data_int = (int *) axis_data;
    for (j = 0; j < ntot; ++j) {
      nccf_get_multi_index(ndims, dims, j, ijk);
      data[j] = axis_data_int[ijk[index_pos]];
    }
  }
  else {
    // error?
  }

  status = nccf_def_coord(ndims, dims, (const char **)dimnames, 
                          data, save, name, standard_name, 
                          units, coordid);
  tot_error += abs(status);

  free(data);
  for (i = 0; i < ndims; ++i) {
    free(dimnames[i]);
  }
  free(dimnames);

  return tot_error;
}
