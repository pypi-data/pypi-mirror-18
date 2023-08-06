/* $Id: nccf_is_coord.c 876 2011-12-16 18:24:04Z pletzer $ */

#include <nccf_constants.h>
#include "nccf_coord.h"
#include <string.h>

/**
 * \ingroup gs_coord_grp
 * Check if coordinate is a longitude 
 * 
 * \param coordid coordinate ID
 * \param yesno (output) 1=yes 0=no
 */
int nccf_is_coord_lon(int coordid, int *yesno) {
  *yesno = 0;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  const char *units;
  const char *standard_name;
  const char *axis;
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_UNITS,
		       (const void **) &units);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_STANDARD_NAME,
		       (const void **) &standard_name);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_AXIS,
		       (const void **) &axis);
  /* CF convention document:
     Variables representing longitude must always explicitly include the 
     units attribute; there is no default value. The units attribute will 
     be a string formatted as per the udunits.dat file. The recommended 
     unit of longitude is degrees_east. Also acceptable are degree_east, 
     degree_E, degrees_E, degreeE, and degreesE. Optionally, the longitude 
     type may be indicated additionally by providing the standard_name 
     attribute with the value longitude, and/or the axis attribute with 
     the value X. 
  */
  if (units) {
    if (strstr(units, "degrees_east") || strstr(units, "degree_east") || 
        strstr(units, "degrees_E") || strstr(units, "degree_E") ||
        strstr(units, "degreesE") || strstr(units, "degreeE")) {
      *yesno = 1;
    }
  }
  if (units && standard_name) {
    if (strstr(standard_name, "longitude") || 
        strstr(standard_name, "grid_longitude")) {
      *yesno = 1;
    }
  }
  if (units && axis) {
    if (strstr(axis, "X")) {
      *yesno = 1;
    }
  }
  return NC_NOERR;
}

/**
 * \ingroup gs_coord_grp
 * Check if coordinate is a latitude 
 * 
 * \param coordid coordinate ID
 * \param yesno (output) 1=yes 0=no
 */
int nccf_is_coord_lat(int coordid, int *yesno) {
  *yesno = 0;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  const char *units;
  const char *standard_name;
  const char *axis;
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_UNITS,
		       (const void **) &units);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_STANDARD_NAME,
		       (const void **) &standard_name);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_AXIS,
		       (const void **) &axis);
  if (units) {
    if (strstr(units, "degrees_north") || strstr(units, "degree_north") || 
        strstr(units, "degrees_N") || strstr(units, "degree_N") ||
        strstr(units, "degreesN") || strstr(units, "degreeN")) {
      *yesno = 1;
    }
  }
  if (units && standard_name) {
    if (strstr(standard_name, "latitude") || 
        strstr(standard_name, "grid_latitude")) {
      *yesno = 1;
    }
  }
  if (units && axis) {
    if (strstr(axis, "Y")) {
      *yesno = 1;
    }
  }
  return NC_NOERR;
}

/**
 * \ingroup gs_coord_grp
 * Check if coordinate is depth/height 
 * 
 * \param coordid coordinate ID
 * \param yesno (output) 1=yes 0=no
 */
int nccf_is_coord_vert(int coordid, int *yesno) {
  *yesno = 0;
  struct nccf_coord_type *self;
  self = nccf_li_find(&CFLIST_COORDINATE, coordid);
  const char *units;
  const char *standard_name;
  const char *axis;
  const char *positive;
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_UNITS,
		       (const void **) &units);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_STANDARD_NAME,
		       (const void **) &standard_name);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_AXIS,
		       (const void **) &axis);
  nccf_varGetAttribPtr(&self->coordVar, CF_ATTNAME_POSITIVE,
		       (const void **) &positive);
  if (units) {
    if (strstr(units, "bar") || 
        strstr(units, "millibar") || 
        strstr(units, "decibar") ||
        strstr(units, "atmosphere") || 
        strstr(units, "atm") ||
        strstr(units, "pascal") || 
        strstr(units, "Pa") || 
        strstr(units, "hPa")) {
      *yesno = 1;
    }
    else if (positive) {
      /* positive attr is required for other than pressure units */
      if (strstr(units, "meter") || 
          strstr(units, "metre") || 
          strstr(units, "m") || 
          strstr(units, "km")) {
        *yesno = 1;
      }
    }
  }
  if (standard_name) {
    /* dimensionless vertical axes, units attribute is not required */
    if (strstr(standard_name, "atmosphere_ln_pressure_coordinate") || 
        strstr(standard_name, "atmosphere_sigma_coordinate") ||
        strstr(standard_name, "atmosphere_sigma_pressure_coordinate") ||
        strstr(standard_name, "atmosphere_hybrid_height_coordinate") ||
        strstr(standard_name, "atmosphere_sleve_coordinate") ||
        strstr(standard_name, "ocean_sigma_coordinate") ||
        strstr(standard_name, "ocean_s_coordinate") ||
        strstr(standard_name, "ocean_sigma_z_coordinate") ||
        strstr(standard_name, "ocean_double_sigma_coordinate")) {
      *yesno = 1;
    }
  }
  if (axis) {
    if (strstr(axis, "Z")) {
      *yesno = 1;
    }
  }
  return NC_NOERR;
}

