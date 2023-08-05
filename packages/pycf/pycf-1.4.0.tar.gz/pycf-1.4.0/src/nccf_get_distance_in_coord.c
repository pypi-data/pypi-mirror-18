/* $Id: nccf_get_distance_in_coord.c 1007 2016-10-10 03:36:23Z pletzer $ 
 * \author Alexander Pletzer, Tech-X Corp.
 */

#include <math.h>
#include <nccf_constants.h>
#include <nccf_utility_functions.h>

#define _TYPE double 
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_double
#define nccf_get_position_TYPE nccf_get_position_double
#define nccf_get_shortest_displ_TYPE nccf_get_shortest_displ_double
#define _HUGE_TYPE CF_HUGE_DOUBLE
#include "nccf_get_distance_in_coord.h"
#undef _HUGE_TYPE
#undef nccf_get_shortest_displ_TYPE
#undef nccf_get_position_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef _TYPE

#define _TYPE float
#define nccf_get_distance_in_coord_TYPE nccf_get_distance_in_coord_float
#define nccf_get_position_TYPE nccf_get_position_float
#define nccf_get_shortest_displ_TYPE nccf_get_shortest_displ_float
#define _HUGE_TYPE CF_HUGE_FLOAT
#include "nccf_get_distance_in_coord.h"
#undef _HUGE_TYPE
#undef nccf_get_shortest_displ_TYPE
#undef nccf_get_position_TYPE
#undef nccf_get_distance_in_coord_TYPE
#undef _TYPE
