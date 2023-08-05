/**
 * $Id: nccf_get_linear_weights.c 651 2011-03-30 22:24:46Z pletzer $
 */

#include <float.h>
#include <math.h>
#include <stdio.h>
#include <netcdf.h>
#include <nccf_utility_functions.h>

#include <assert.h> // DEBUG

#define nccf_get_linear_weights_TYPE nccf_get_linear_weights_double
#define _TYPE double
#define _EPS (10*DBL_EPSILON)
#define nccf_solve_TYPE nccf_solve_double
#include <nccf_get_linear_weights.h>
#undef nccf_solve_TYPE
#undef _EPS
#undef _TYPE
#undef nccf_get_linear_weights_TYPE

#define nccf_get_linear_weights_TYPE nccf_get_linear_weights_float
#define _TYPE float
#define _EPS (10*FLT_EPSILON)
#define nccf_solve_TYPE nccf_solve_float
#include <nccf_get_linear_weights.h>
#undef nccf_solve_TYPE
#undef _EPS
#undef _TYPE
#undef nccf_get_linear_weights_TYPE

