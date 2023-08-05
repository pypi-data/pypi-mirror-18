/**
 * $Id: nccf_determinant.c 1007 2016-10-10 03:36:23Z pletzer $
 */

#include <nccf_utility_functions.h>

#define _TYPE double
#define nccf_determinant_TYPE nccf_determinant_double
#define _GETRF dGetrf
#include <nccf_determinant.h>
#undef _GETRF
#undef nccf_determinant_TYPE
#undef _TYPE

#define _TYPE float
#define nccf_determinant_TYPE nccf_determinant_float
#define _GETRF fGetrf
#include <nccf_determinant.h>
#undef _GETRF
#undef nccf_determinant_TYPE
#undef _TYPE

