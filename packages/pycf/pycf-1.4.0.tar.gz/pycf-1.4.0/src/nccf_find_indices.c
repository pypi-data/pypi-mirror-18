/**
 * $Id: nccf_find_indices.c 905 2011-12-29 04:56:48Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <nccf_utility_functions.h>

#include <cf_config.h>

#define nccf_find_indices_TYPE nccf_find_indices_double
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_double
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_double
#define nccf_find_next_indices_TYPE nccf_find_next_indices_double
#define nccf_linesearch_indices_TYPE nccf_linesearch_indices_double
#define _TYPE double
#include <nccf_find_indices.h>
#undef _TYPE
#undef nccf_linesearch_indices_TYPE
#undef nccf_find_next_indices_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef nccf_find_indices_TYPE

#define nccf_find_indices_TYPE nccf_find_indices_float
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_float
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_float
#define nccf_find_next_indices_TYPE nccf_find_next_indices_float
#define nccf_linesearch_indices_TYPE nccf_linesearch_indices_float
#define _TYPE float
#include <nccf_find_indices.h>
#undef _TYPE
#undef nccf_linesearch_indices_TYPE
#undef nccf_find_next_indices_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef nccf_find_indices_TYPE




