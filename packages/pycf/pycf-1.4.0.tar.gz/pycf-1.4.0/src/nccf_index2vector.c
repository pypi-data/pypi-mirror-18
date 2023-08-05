/**
 * PURPOSE: Convert an index into a vector of -1, 0, and 1
 * \author Dave Kindig, Tech-X Corp.
 * "$Id: nccf_index2vector.c 467 2011-01-27 07:17:59Z dkindig $"
 */

#include <stdio.h>
#include <math.h>

int nccf_index2vector(int index, int ndims, int vector[]){

    int mod, div, sign;
    int i;

/* Normal vector +/- */
    div = index / 2;   
    mod = index % 2;

    switch (mod) {
      case 0: 
        sign = -1;
        break;
      default:
      /* mod is 1 */
      sign =  1;
    }

    /* Zero out the vector*/
    for( i = 0; i < ndims; i++ ){
      vector[i] = 0;
    }

    /* Populate the vector */
    vector[div] = 1 * sign;

    return 0;
}
