/**
 * Perform line search in index space
 * $Id: nccf_linesearch_indices.c 905 2011-12-29 04:56:48Z pletzer $
 *
 * \author Alexander Pletzer
 */

#include <stdlib.h>
#include <math.h>
#include <nccf_utility_functions.h>

#define nccf_linesearch_indices_TYPE nccf_linesearch_indices_double
#define _TYPE double
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_double
#include <nccf_linesearch_indices.h>
#undef nccf_get_distance_in_coord_TYPE
#undef _TYPE
#undef nccf_linesearch_indices_TYPE

#define nccf_linesearch_indices_TYPE nccf_linesearch_indices_float
#define _TYPE float
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_float
#include <nccf_linesearch_indices.h>
#undef nccf_get_distance_in_coord_TYPE
#undef _TYPE
#undef nccf_linesearch_indices_TYPE

