/**
 * $Id: nccf_linear_interp_mod.c 915 2012-01-09 16:58:08Z pletzer $
 */

#include <netcdf.h>
#include <math.h>
#include <nccf_utility_functions.h>
#include <nccf_constants.h>

#define nccf_linear_interp_mod_TYPE nccf_linear_interp_mod_double
#define _TYPE double
#include <nccf_linear_interp_mod.h>
#undef _TYPE
#undef nccf_linear_interp_mod_TYPE

#define nccf_linear_interp_mod_TYPE nccf_linear_interp_mod_float
#define _TYPE float
#include <nccf_linear_interp_mod.h>
#undef _TYPE
#undef nccf_linear_interp_mod_TYPE
