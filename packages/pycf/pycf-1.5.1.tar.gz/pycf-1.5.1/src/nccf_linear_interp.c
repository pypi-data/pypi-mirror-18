/**
 * $Id: nccf_linear_interp.c 628 2011-03-28 16:52:19Z pletzer $
 */

#include <netcdf.h>
#include <math.h>
#include <nccf_utility_functions.h>

#define nccf_linear_interp_TYPE nccf_linear_interp_double
#define _TYPE double
#include <nccf_linear_interp.h>
#undef _TYPE
#undef nccf_linear_interp_TYPE

#define nccf_linear_interp_TYPE nccf_linear_interp_float
#define _TYPE float
#include <nccf_linear_interp.h>
#undef _TYPE
#undef nccf_linear_interp_TYPE
