/*
 * Find next index adjacent to current index without repetition. 
 * This routine assumes the fastest varying index is the last index
 *
 * \author Dave Kindig, Tech-X Corp.
 *
 * $Id: nccf_find_next_adjcnt_index.c 881 2011-12-17 21:53:14Z pletzer $
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <nccf_utility_functions.h>

#include <cf_config.h>

int 
nccf_find_next_adjcnt_index( int ndims, const int dims[], 
			     int kji[] ){

  int m, n, index, mult = 1;
  int *tmp_dims, *tmp_locs, kjiFI, currFI, di1 = 0, di2 = 0;

  int flatIndices[ndims];
  int directionVectors[ndims][ndims];
  int dir[ndims];

  /* Returns */
  int inside_domain = 1; 
  int isCorner  =  0;

  /* Set up the directionVectors */
  directionVectors[0][0] = 1;
  for( m = 0; m < ndims-1; m++ ){
    mult *= (1 - 2 * ( kji[m] % 2 ));
    directionVectors[m+1][m+1] = mult;
  }

  /* Calculate the flat index of the location */
  int fi;
  for( m = ndims-1; m >= 0 ; m-- ){
    tmp_dims = (int *)malloc((m+1) * sizeof(int));
    tmp_locs = (int *)malloc((m+1) * sizeof(int));
    for( n = 0; n < m+1; n++ ) tmp_dims[n] = dims[n];
    for( n = 0; n < m+1; n++ ) tmp_locs[n] = dims[n]-1;
    fi = nccf_get_flat_index( m+1, tmp_dims, tmp_locs );
    index = (ndims-m)-1;
    flatIndices[index] = fi;
    free( tmp_dims );
    free( tmp_locs );
  }

  /* Determine if location vector is inside the domain by finding the adjacent
   * location vector location vector is updated as well */

  /* For higher dimensions, corners are special in some cases */
  if( ndims > 1 ){
    if( kji[ndims-2] == 0 && kji[ndims-1] == 0 ){
      if (directionVectors[ndims-1][ndims-1] == -1) isCorner = 1;
    }
    if( kji[ndims-2] == dims[ndims-2]-1 && kji[ndims-1] == 0 ){
      if (directionVectors[ndims-1][ndims-1] == -1) isCorner = 1;
    }
    /* Even top row */
    if( (kji[ndims-2] % 2) == 1 ){
      if( kji[ndims-2] == 0 && kji[ndims-1] == dims[ndims-1]-1 ){
        if (directionVectors[ndims-1][ndims-1] == +1) isCorner = 1;
      }
    }
    /* Odd  top row */
    if( (kji[ndims-2] % 2) == 0 ){
      if( kji[ndims-2] == dims[ndims-2]-1 && kji[ndims-1] == dims[ndims-1]-1 ){
        if (directionVectors[ndims-1][ndims-1] == +1) isCorner = 1;
      }
    }

    /* Found a corner */
    if( isCorner == 1 && ndims == 2 ){
      inside_domain = 0;
      kji[0] = kji[0] + directionVectors[0][0];
      return inside_domain;
    }
    else if( isCorner && ndims > 1 ){
      for( m = 0; m < ndims-2; m++ ){
        /* If the dimension of i is max'd out then the location is outside of
         * the domain otherwise just increment the index by 1 */
        if( kji[m] != dims[m]-1 ){
          kji[m] = kji[m] + 1;
          return inside_domain;
        }
        else{
          inside_domain = 0;
          kji[m] = kji[m] + 1;
          return inside_domain;
        }
      }
    }
  }

  /* Deal with non corners */
  for( m = 0; m < ndims; m++ ) dir[m] = directionVectors[m][m];

  kjiFI = nccf_get_flat_index( ndims, dims, kji );

  /* Ignore the i-dimension */
  for( m = ndims-1; m >= 1; m-- ){
    currFI = flatIndices[m];
    if( dir[m-1] > 0) di1 = 1;
    if( dir[m-1] < 0) di2 = 1;
    if( isCorner == 0 ){
      if( kjiFI % (currFI+1) == 0 && (kji[m-1] % 2) == 1 && di1 == 1 ){
        kji[m-1] = kji[m-1] + dir[m-1];
        if( kji[m-1] > dims[m-1]-1 ) return 0;
        return inside_domain;
      }
      if( kjiFI % (currFI+1) == 0 && (kji[m-1] % 2 == 0) && di2 == 1 ){
        kji[m-1] = kji[m-1] + dir[m-1];
        if( kji[m-1] > dims[m-1]-1 ) return 0;
        return inside_domain;
      }
      if( kjiFI % (currFI+1) == currFI && (kji[m-1] % 2) == 0 && di1 == 1 ){
        kji[m-1] = kji[m-1] + dir[m-1];
        if( kji[m-1] > dims[m-1]-1 ) return 0;
        return inside_domain;
      }
      if( kjiFI % (currFI+1) == currFI && (kji[m-1] % 2) == 1 && di2 == 1 ){
        kji[m-1] = kji[m-1] + dir[m-1];
        if( kji[m-1] > dims[m-1]-1 ) return 0;
        return inside_domain;
      }
    }
  }

  kji[ndims-1] = kji[ndims-1] + dir[ndims-1];
  
  /* Clean up */

  return inside_domain;

}
