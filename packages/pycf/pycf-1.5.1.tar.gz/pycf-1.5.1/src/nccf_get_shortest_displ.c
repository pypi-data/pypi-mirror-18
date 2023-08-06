/**
 * $Id: nccf_find_next_indices.c 903 2011-12-28 21:46:08Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <nccf_utility_functions.h>
#include <nccf_constants.h>

#include <cf_config.h>

#define nccf_get_shortest_displ_TYPE nccf_get_shortest_displ_double
#define _TYPE double
#define _HUGE_TYPE CF_HUGE_DOUBLE
#include <nccf_get_shortest_displ.h>
#undef _HUGE_TYPE
#undef _TYPE
#undef nccf_get_shortest_displ_TYPE

#define nccf_get_shortest_displ_TYPE nccf_get_shortest_displ_float
#define _TYPE float
#define _HUGE_TYPE CF_HUGE_FLOAT
#include <nccf_get_shortest_displ.h>
#undef _HUGE_TYPE
#undef _TYPE
#undef nccf_get_shortest_displ_TYPE



