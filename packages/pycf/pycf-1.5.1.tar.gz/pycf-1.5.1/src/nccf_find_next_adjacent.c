/*
 * Find the next cell adjacent to the current cell in using k, j, i order
 *
 * $Id: nccf_find_next_adjacent.c 373 2011-01-14 19:53:49Z pletzer $
 */

int nccf_find_next_adjacent( int ndims, const int dims[], int kji[] ){

  int z, inside_domain = 1, mult = 1;

  /* Calculate the Direction vector */
  int directionVector[ndims], tmpkji;
  directionVector[0] = 1;
  for( z = 0; z < ndims-1; z++ ){
    mult *= (1 - 2 * ( kji[z] % 2 ));
    directionVector[z+1] = mult;
  }

  /* Start at the fastest varying dimension */
  for( z = ndims-1; z >= 0; z-- ){
    tmpkji = kji[z] + directionVector[z]; 
    if( tmpkji >= 0 ){
      if( tmpkji <= dims[z]-1 ){
        kji[z] = kji[z] + directionVector[z];
        return inside_domain;
      }
    }
  }

  inside_domain = 0;
  return inside_domain;

}

