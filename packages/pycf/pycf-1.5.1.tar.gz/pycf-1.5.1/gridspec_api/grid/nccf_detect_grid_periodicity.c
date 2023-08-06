/* $Id: nccf_detect_grid_periodicity.c 943 2016-09-05 03:10:31Z pletzer $ */

#include <nccf_constants.h>
#include <nccf_utility_functions.h>
#include <nccf_coord.h>
#include "nccf_grid.h"
#include <string.h>
#include <math.h>
#include <stdlib.h>

int nccf_detect_grid_periodicity(struct nccf_struct_grid_type *self) {

  int status, i, islon;
  int toterr = 0;
  char units[STRING_SIZE];

  free(self->coord_periodicity);
  self->coord_periodicity = (double *) malloc(self->ndims * sizeof(double));
 
  for(i = 0; i < self->ndims; ++i) {
    /* set the periodicity lengths, default are very large numbers  */
    self->coord_periodicity[i] = CF_HUGE_DOUBLE;
    islon = 0;
    status = nccf_is_coord_lon(self->coordids[i], &islon);
    toterr += abs(status);
    if (islon) {
      status = nccf_inq_coord_units(self->coordids[i], units);
      /* units of longitudes can be radians, so test */
      if (strncmp(units, "degree", 6) == 0)  {
        self->coord_periodicity[i] = 360.0;
      }
      else {
        self->coord_periodicity[i] = M_2_PI;
      } 
    }
  }

  return toterr;
}
