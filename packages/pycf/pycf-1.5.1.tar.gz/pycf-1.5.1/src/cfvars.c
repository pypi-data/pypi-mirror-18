/* This file handles the libcf variable functions. */

#include <cf_config.h>
#include <libcf_src.h>
#include <libcf_int.h>
#include <netcdf.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int nccf_parse_coords(int ncid, int varid, char *att_name, int *naxes, 
		      int *axis_varids);
int
nccf_def_var1(int ncid, int varid, const char *units, 
	     const char *long_name, const char *standard_name, 
	     int ncoord_vars, int *coord_varids)
{
   return nccf_def_var(ncid, varid, units, long_name, standard_name, 0, NULL);
}

/*! \defgroup var_grp Variable-Level Functions
@{*/

/*! Define the recomended attributes for a data variable.

  From the CF conventions, 1.0:

  'Each variable in a netCDF file has an associated description which is
  provided by the attributes units, long_name, and standard_name. The
  units, and long_name attributes are defined in the NUG and the
  standard_name attribute is defined in this document.'

  also

  'We wish to allow ... institution, source, references, and comment, to
  be either global or assigned to individual variables. When an
  attribute appears both globally and as a variable attribute, the
  variable's version has precedence.'

  also

  'The value of the coordinates attribute is a blank separated list of
  the names of auxiliary coordinate variables.'

  This function makes all of these optional.

  \param ncid
  The ncid of the file.

  \param varid
  The varid of the netCDF variable being described.

  \param units
  If non-NULL, this text string will be written as the CF-recommended
  ``units'' attribute.

  \param long_name
  If non-NULL, this text string will be written as the CF-recommended
  ``long_name'' attribute.

  \param standard_name
  If non-NULL, this text string will be written as the CF-recommended
  ``standard_name'' attribute.

  \param ncoord_vars
  Number of coordinate variables for this variable.

  \param coord_varids
  The variable IDs of the coordinate variables for this variable.

  \return 0 on success, error code otherwise

  \author Ed Hartnett, Unidata
*/
int
nccf_def_var(int ncid, int varid, const char *units, 
	     const char *long_name, const char *standard_name, 
	     int ncoord_vars, int *coord_varids)
{
   char coord_name[NC_MAX_NAME + 1];
   char coords_str[CF_MAX_COORD_LEN + 1];
   int c, ret;

   /* Write units. */
   if (units)
      if ((ret = nc_put_att_text(ncid, varid, CF_UNITS,
				 strlen(units) + 1, units)))
	 return ret;

   /* Write long_name. */
   if (long_name)
      if ((ret = nc_put_att_text(ncid, varid, CF_LONG_NAME,
				 strlen(long_name) + 1, long_name)))
	 return ret;

   /* Write standard_name. */
   if (standard_name)
      if ((ret = nc_put_att_text(ncid, varid, CF_STANDARD_NAME,
				 strlen(standard_name) + 1, standard_name)))
	 return ret;

   /* Now add the "coordinates" atttribute, which holds a space
    * separated list of auxilary coordinate variables. */
   if (ncoord_vars)
   {
      if (ncoord_vars > CF_MAX_COORDS)
	 return CF_EMAXCOORDS;
      if (!coord_varids) 
	 return CF_EINVAL;
      strcpy(coords_str, "");
      for (c = 0; c < ncoord_vars; c++)
      {
	 /* Find the names of this coordinate var. */
	 if ((ret = nc_inq_varname(ncid, coord_varids[c], coord_name)))
	    return ret;
	 strcat(coords_str, coord_name);
	 strcat(coords_str, " ");
      }
      if ((ret = nc_put_att_text(ncid, varid, CF_COORDINATES,
				 strlen(coords_str) + 1, coords_str)))
	 return ret;
   }
   
   return NC_NOERR;
}

/*! Read the CF annotations of a variable. 

    Recall that in C, strlens do not include the null terminator. To
    get the lengths before the strings (in order to allocatate) pass
    NULL for any or all strngs and the lengths will be returned. Then
    call the funtion again after allocating memory.  Any of these
    pointer args may be NULL, in which case it will be ignored.

    \param ncid the ncid of the file

    \param varid the varid of the variable

    \param units_lenp if non-NULL, length of units string will be
    copied here.

    \param units if non-NULL, units string will be copied here

    \param long_name_lenp if non-NULL, length of long_name string will be
    copied here.

    \param long_name if non-NULL, long_name string will be copied here

    \param standard_name_lenp if non-NULL, length of standard_name string will be
    copied here.

    \param standard_name if non-NULL, standard_name string will be copied here

    \param ncoord_vars if non-NULL, the number of coordinate variables will be
    copied here.

    \param coord_varids if non-NULL, the varids of the coordinate
    variables will be copied here

   \return 0 on success, error code otherwise

   \author Ed Hartnett, Unidata

*/
int
nccf_inq_var(int ncid, int varid,
	     size_t *units_lenp, char *units, 
	     size_t *long_name_lenp, char *long_name,
	     size_t *standard_name_lenp, char *standard_name,
	     int *ncoord_vars, int *coord_varids)
{
   int ret;

   /* Read units length if desired. */
   if (units_lenp)
   {
      if ((ret = nc_inq_attlen(ncid, varid, CF_UNITS, units_lenp)) == NC_ENOTATT)
	 *units_lenp = 0;
      else if (ret)
	 return ret;
   }

   /* Read units value if desired. */
   if (units)
   {
      if ((ret = nc_get_att_text(ncid, varid, CF_UNITS, units)) == NC_ENOTATT)
	 strcpy(units, "");
      else if (ret)
	 return ret;
   }

   if (long_name_lenp)
   {
      if ((ret = nc_inq_attlen(ncid, varid, CF_LONG_NAME, 
			       long_name_lenp)) == NC_ENOTATT)
	 *long_name_lenp = 0;
      else if (ret)
	 return ret;
   }

   if (long_name)
   {
      if ((ret = nc_get_att_text(ncid, varid, CF_LONG_NAME, long_name)) == NC_ENOTATT)
	 strcpy(long_name, "");
      else if (ret)
	 return ret;
   }

   if (standard_name_lenp)
   {
      if ((ret = nc_inq_attlen(ncid, varid, CF_STANDARD_NAME, 
			       standard_name_lenp)) == NC_ENOTATT)
	 *standard_name_lenp = 0;
      else if (ret)
	 return ret;
   }

   if (standard_name)
   {
      if ((ret = nc_get_att_text(ncid, varid, CF_STANDARD_NAME,
				 standard_name)) == NC_ENOTATT)
	 strcpy(standard_name, "");
      else if (ret)
	 return ret;
   }

   /* Learn the number of coordinate variables, and their IDs, if
    * desired. */
   if ((ret = nccf_parse_coords(ncid, varid, CF_COORDINATES, 
				ncoord_vars, coord_varids)) == NC_ENOTATT)
   {
      if (ncoord_vars) 
	 *ncoord_vars = 0;
   }
   else if (ret)
      return ret;
      
   return NC_NOERR;
}

/*! Define missing data information for a variable.

   This function sets the ``fill_value'', ``valid_min'', and
   ``valid_max'' attributes.

   \param ncid The ncid of the netCDF file.

   \param varid The varid of the netCDF variable being described.

   \param fill_value If non-NULL, this will point to a value of the
   same type as this varid, which will be used as the fill_value for
   the data.

   \param valid_min If non-NULL, this will point to a value of the
   same type as this varid, which will be written as the ``valid_min''
   attribute. If this parameter is non-NULL, valid_max must also be
   provided.

   \param valid_max If non-NULL, this will point to a value of the same type as this
   varid, which will be written as the ``valid_max'' attribute. If this
   parameter is non-NULL, valid_min must also be provided.

   \return 0 on success, error code otherwise

   \author Ed Hartnett, Unidata
*/
int 
nccf_def_var_missing(int ncid, int varid, const void *fill_value, 
		     const void *valid_min, const void *valid_max)
{
   nc_type xtype;
   int ret;

   /* User must provide either both or neither of valid_minp and
    * valid_max. */
   if ((valid_min && !valid_max) || 
       (!valid_min && valid_max))
      return CF_EMINMAX;

   /* Get the variable type. */
   if ((ret = nc_inq_vartype(ncid, varid, &xtype)))
      return ret;

   /* Write a fill value if the user provided one. */
   if (fill_value)
      if ((ret = nc_put_att(ncid, varid, CF_FILL_VALUE, 
			    xtype, 1, fill_value)))
	 return ret;

   /* Write a valid_min if the user provided one. */
   if (valid_min)
      if ((ret = nc_put_att(ncid, varid, CF_VALID_MIN, 
			    xtype, 1, valid_min)))
	 return ret;

   /* Write a valid_max value if the user provided one. */
   if (valid_max)
      if ((ret = nc_put_att(ncid, varid, CF_VALID_MAX, 
			    xtype, 1, valid_max)))
	 return ret;
      
   return NC_NOERR;
}

/* Return the default fill value of a netCDF-3 type. */
static int
nccf_get_default_missing(nc_type xtype, void *fill_value, 
			 void *valid_min, void *valid_max)
{
   /* At the moment, only handle netCDF-3 types. */
   switch(xtype)
   {
      case NC_BYTE:
	 if (fill_value)
	    *((signed char *)fill_value) = NC_FILL_BYTE;
	 if (valid_min)
	    *((signed char *)valid_min) = CF_BYTE_MIN;
	 if (valid_max)
	    *((signed char *)valid_max) = CF_BYTE_MAX;
	 break;
      case NC_CHAR:
	 if (fill_value)
	    *((char *)fill_value) = NC_FILL_CHAR;
	 if (valid_min)
	    *((char *)valid_min) = CF_CHAR_MIN;
	 if (valid_max)
	    *((char *)valid_max) = CF_CHAR_MAX;
	 break;
      case NC_SHORT:
	 if (fill_value)
	    *((short *)fill_value) = NC_FILL_SHORT;
	 if (valid_min)
	    *((short *)valid_min) = CF_SHORT_MIN;
	 if (valid_max)
	    *((short *)valid_max) = CF_SHORT_MAX;
	 break;
      case NC_INT:
	 if (fill_value)
	    *((int *)fill_value) = NC_FILL_INT;
	 if (valid_min)
	    *((int *)valid_min) = CF_INT_MIN;
	 if (valid_max)
	    *((int *)valid_max) = CF_INT_MAX;
	 break;
      case NC_FLOAT:
	 if (fill_value)
	    *((float *)fill_value) = NC_FILL_FLOAT;
	 if (valid_min)
	    *((float *)valid_min) = CF_FLOAT_MIN;
	 if (valid_max)
	    *((float *)valid_max) = CF_FLOAT_MAX;
	 break;
      case NC_DOUBLE:
	 if (fill_value)
	    *((double *)fill_value) = NC_FILL_DOUBLE;
	 if (valid_min)
	    *((double *)valid_min) = CF_DOUBLE_MIN;
	 if (valid_max)
	    *((double *)valid_max) = CF_DOUBLE_MAX;
	 break;
      default:
	 return CF_EBADTYPE;
   }

   return NC_NOERR;
}

/*! Get attributes which define missing data information. If the
   attributes are not there, then provide the valid data anyway, based
   on netCDF defaults.

   \param ncid The ncid of the file.

   \param varid The varid of the netCDF variable.

   \param fill_value If this is not NULL, the fill value of the
   variable will be written at this address by
   nccf_inq_var_missing. If the fill value was not defined for the
   variable, the netCDF default value will be used.

   \param valid_min If this is not NULL, the valid_min value of the
   variable will be written at this address by
   nccf_inq_var_missing. If the valid_min was not defined for the
   variable, the netCDF default value will be used.

   \param valid_max If this is not NULL, the valid_max value of the
   variable will be written at this address by
   nccf_inq_var_missing. If the valid_max value was not defined for
   the variable, the netCDF default value will be used.

   \return 0 on success, error code otherwise

   \author Ed Hartnett, Unidata
*/
int 
nccf_inq_var_missing(int ncid, int varid, void *fill_value, 
		     void *valid_min, void *valid_max)
{
   nc_type xtype;
   int ret;

   if ((ret = nc_inq_vartype(ncid, varid, &xtype)))
      return ret;

   /* Does the user want the fill value?*/
   if (fill_value)
   {
      /* Get the value of the _FillValue att, if it is there. */
      ret = nc_get_att(ncid, varid, CF_FILL_VALUE, fill_value);
      if (ret == NC_ENOTATT)
      {
	 /* No _FillValue att, so find the default fill value for this
	  * type. */
	 if ((ret = nccf_get_default_missing(xtype, fill_value, NULL, NULL)))
	    return ret;
      }
      else if (ret != NC_NOERR)
	 return ret;
   }

   /* Does the user want the fill value?*/
   if (valid_min)
   {
      /* Get the value of the valid_min, if it is there. */
      ret = nc_get_att(ncid, varid, CF_VALID_MIN, valid_min);
      if (ret == NC_ENOTATT)
      {
	 /* No _FillValue att, so find the default fill value for this
	  * type. */
	 if ((ret = nccf_get_default_missing(xtype, NULL, valid_min, NULL)))
	    return ret;
      }
      else if (ret != NC_NOERR)
	 return ret;
   }

   /* Does the user want the fill value?*/
   if (valid_max)
   {
      /* Get the value of the _FillValue att, if it is there. */
      ret = nc_get_att(ncid, varid, CF_VALID_MAX, valid_max);
      if (ret == NC_ENOTATT)
      {
	 /* No _FillValue att, so find the default fill value for this
	  * type. */
	 if ((ret = nccf_get_default_missing(xtype, NULL, NULL, valid_max)))
	    return ret;
      }
      else if (ret != NC_NOERR)
	 return ret;
   }

   return NC_NOERR;
}

/*!@}*/
