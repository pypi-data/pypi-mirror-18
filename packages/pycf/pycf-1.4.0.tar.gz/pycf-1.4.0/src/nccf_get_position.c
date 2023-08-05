/**
 * $Id: nccf_get_position.c 905 2011-12-29 04:56:48Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

#include <stdlib.h>
#include <math.h>
#include <netcdf.h> // for NC_FILL_DOUBLE, ...
#include <nccf_utility_functions.h>
#include <nccf_constants.h>

#define nccf_get_position_TYPE nccf_get_position_double
#define _TYPE double
#define _FILL_VALUE NC_FILL_DOUBLE
#define nccf_linear_interp_TYPE nccf_linear_interp_double
#define nccf_linear_interp_mod_TYPE nccf_linear_interp_mod_double
#define nccf_get_linear_weights_TYPE nccf_get_linear_weights_double
#define _HUGE_TYPE CF_HUGE_DOUBLE
#include <nccf_get_position.h>
#undef _HUGE_TYPE
#undef nccf_get_linear_weights_TYPE
#undef nccf_linear_interp_mod_TYPE
#undef nccf_linear_interp_TYPE
#undef _FILL_VALUE
#undef _TYPE
#undef nccf_get_position_TYPE

#define nccf_get_position_TYPE nccf_get_position_float
#define _TYPE float
#define _FILL_VALUE NC_FILL_FLOAT
#define nccf_linear_interp_TYPE nccf_linear_interp_float
#define nccf_linear_interp_mod_TYPE nccf_linear_interp_mod_float
#define nccf_get_linear_weights_TYPE nccf_get_linear_weights_float
#define _HUGE_TYPE CF_HUGE_FLOAT
#include <nccf_get_position.h>
#undef _HUGE_TYPE
#undef nccf_get_linear_weights_TYPE
#undef nccf_linear_interp_mod_TYPE
#undef nccf_linear_interp_TYPE
#undef _FILL_VALUE
#undef _TYPE
#undef nccf_get_position_TYPE

