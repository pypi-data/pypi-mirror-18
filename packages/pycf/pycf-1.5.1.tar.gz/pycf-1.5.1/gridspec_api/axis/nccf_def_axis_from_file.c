/*
 * $Id: nccf_def_axis_from_file.c 982 2016-09-27 03:33:00Z pletzer $
 */

#include "nccf_axis.h"
#include <stdlib.h>
#include <string.h>

#include <nccf_handle_error.h>
#include <nccf_varObj.h>

/**
 * \ingroup gs_axis_grp
 * Define a coordinate axis from file (constructor).
 *
 * \param filename file name
 * \param name name of the object
 * \param axisid object ID (output)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer (Tech-X Corp.) and Ed Hartnett (UCAR).
 */

int nccf_def_axis_from_file(const char *filename, const char *name,
                            int *axisid) {

  int totError = NC_NOERR;
  int ncid, status = NC_NOERR;
  struct nccf_var_obj *v;

  // read the variable
  status = nc_open(filename, NC_NOWRITE, &ncid);
  if (status) return status;
  totError += abs(status);
  // note: data will be cast as doubles
  nccf_varCreateFromFile(&v, name, ncid, 1, 1);
  status = nc_close(ncid);
  totError += abs(status);

  // build the object
  nc_type xtype = NC_NAT;
  void *data = NULL;
  int *dims;
  const char *standard_name;
  const char *units;
  int positive_up = 1;
  const char *axis = NULL;
  const char *axis_up = NULL;
  const char *formula_terms = NULL;
  
  nccf_varGetDimsPtr(&v, &dims);

  /* Read the rest of the variable */
  nccf_varGetDataType(&v, &xtype);
  nccf_varGetDataPtr(&v, &data);
  nccf_varGetAttribPtr(&v, CF_ATTNAME_STANDARD_NAME, 
		       (const void **) &standard_name);
  nccf_varGetAttribPtr(&v, CF_ATTNAME_UNITS, 
		       (const void **) &units);
  nccf_varGetAttribPtr(&v, CF_AXIS, 
                       (const void **) &axis);
  nccf_varGetAttribPtr(&v, CF_POSITIVE, 
                       (const void **) &axis_up);
  nccf_varGetAttribPtr(&v, CF_FORMULA_TERMS, 
		       (const void **) &formula_terms);
  
  if (axis_up && strcmp(axis_up, CF_DOWN) == 0) {
    positive_up = 0;
  }

  status = nccf_def_axis(name, dims[0], xtype, data, standard_name,
                         units, axis, positive_up, 
                         formula_terms, axisid);
  totError += abs(status);

  // clean up
  nccf_varDestroy(&v);

  return totError;
}
