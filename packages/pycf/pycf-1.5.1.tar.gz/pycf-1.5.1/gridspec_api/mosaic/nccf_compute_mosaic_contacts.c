/********************************************************
  * Set the contact indices for a given contact.
  *
  * $Id: nccf_def_mosaic.c 719 2011-04-26 17:39:51Z srinath22 $
  *
  */

#include "nccf_mosaic.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <libcf_src.h>
#include <netcdf.h>
#include <nccf_grid.h>
#include <nccf_coord.h>
#include <nccf_utility_functions.h>
#include <nccf_constants.h>
#include <nccf_handle_error.h>
#include <nccf_varObj.h>
#include <cflistitem.h>

#define EPSLN 1.e-10  /* Define zero as |val| < EPSLN... */
#define min( a, b ) ( a<b ? a : b )

int nccf_local_do_flipped(int ndims, double begPos1[], double endPos1[]){

  /* Need to compare the dimensions to see if there is rotation
   * This will rewrite the Positions to match IFF there is rotation */

  double *bp1, *ep1;
  int i;

  bp1 = (double *)malloc(ndims * sizeof(double));
  ep1 = (double *)malloc(ndims * sizeof(double));

  for( i = 0; i < ndims; i++ ){
    bp1[i] = endPos1[i];
    ep1[i] = begPos1[i];
  }
  for( i = 0; i < ndims; i++ ){
    begPos1[i] = bp1[i];
    endPos1[i] = ep1[i];
  }

  free( bp1 );
  free( ep1 );

  return NC_NOERR;
}

int nccf_local_check_contact(int ndims, double tol, const double period[],
           const double begPos0[], const double endPos0[],
           const double begPos1[], const double endPos1[]) {
  /* 1 means there is a contact */
  int res = 1;
  int i;
  double begDiff = 0, endDiff = 0, period_test = 0;

  /* It is possible that the 0 dimension
   * will match the 1 dimension and vice versa */
  /* Check for rotation */
  for ( i = 0; i < ndims; ++i ) {
    if(( begPos1[i] - begPos0[i] ) == period[i] ){
      period_test = begPos1[i] - begPos0[i];
    }
    if (( period[i] > 0.0 ) && ( begPos1[i] == endPos1[i] ) &&
       ((( period_test ) == period[i] ) ||
        (( endPos1[i] - endPos0[i] ) == period[i] ))){
  /* coordinates are periodic */
      if( period_test == period[i] ){
        begDiff = fmod(( begPos1[i]-period[i] ), begPos0[i] );
        endDiff = fmod(( endPos1[i]-period[i] ), endPos0[i] );
      }
      else{
        begDiff = fabs( begPos1[i] - begPos0[i] );
        endDiff = fabs( endPos1[i] - endPos0[i] );
      }
    }
    else {
  /* no periodicity */
      begDiff = fabs( begPos1[i] - begPos0[i]);
      endDiff = fabs( endPos1[i] - endPos0[i]);
    }
    if ( begDiff > tol || endDiff > tol ) {
  /* no contact */
      res *= 0;
    }
  }
  //printf("contact=%i\n\n",res );
  return res;
}

/*! \defgroup gs_mosaic_grp Mosaic connectivity
  \ingroup gridspec_grp

The mosaic contains all the connectivity information between tile grids. 
Thus, a mosaic must know about its underlying grids and these must
exist prior to the construction of a mosaic. Grid objects should not
be freed before all operations on the mosaic have been completed.

*/

/**
 * \ingroup gs_mosaic_grp
 * Infer the contacts based on comparing endpoints from adjacent tiles.
 *
 * \param mosaicid a mosaic ID (e.g. returned by nccf_def_mosaic)
 * \param period periodicity array, one element for each dimension. A value of 0 means no periodicity. Must be of type double
 */
int nccf_compute_mosaic_contacts( int mosaicid, const double period[] ){

  /* Open the mosaic structure */
  struct nccf_mosaic_type *self;
  self = nccf_li_find( &CFLIST_MOSAIC, mosaicid );

  int ndims, *dims;
  int *normVec0, *normVec1;
  double *begPos0, *begPos1, *endPos0, *endPos1;
  int *begInd0, *begInd1, *endInd0, *endInd1;
  double *dataPtr;
  double sumPeriods;

  /* flat indices */
  int begIndex0, endIndex0, begIndex1, endIndex1;

  int iedge0, iedge1;
  int iGrid0, iGrid1;
  char *file0, *file1;
  int i;
  int status;
  int isContact = 0, is1Flipped = 0;

  char slice0[STRING_SIZE], slice1[STRING_SIZE];
  char *contactStr, *gridStr;
  char **coordnamesbuffer   = NULL;

  /* Get dimensionality */
  nccf_inq_grid_ndims(self->gridids[0], &ndims);
  self->ndims = ndims;
  int coordIds0[ndims], coordIds1[ndims];
  dims = (int *) malloc(ndims * sizeof(int));

  /* Allocate some strings */
  file1 = (char*)calloc( STRING_SIZE, sizeof( char ));
  coordnamesbuffer = malloc(ndims * sizeof(char *));
  for (i = 0; i < ndims; ++i) {
    coordnamesbuffer[i] = (char *) calloc(STRING_SIZE, sizeof(char));
  }

  /* Populate the coordnames list */
  status = nccf_inq_grid_coordnames(self->gridids[0], coordnamesbuffer);
  for( i = 0; i < ndims; i++ ){
    nccf_li_add(&self->coordnameslist, coordnamesbuffer[i]);
    //free(coordnamesbuffer[i]);
  }
  free(coordnamesbuffer);

  sumPeriods = 0.0;
  for ( i = 0; i < ndims; ++i ) {
    sumPeriods += period[i];
  }

  /* Normal vector of -1, 0, and 1 */
  normVec0 = ( int * ) malloc( ndims * sizeof( int ));
  normVec1 = ( int * ) malloc( ndims * sizeof( int ));

  /* Index values at the start/end corner of the boundary */
  begInd0 = (int *) malloc(ndims * sizeof(int));
  begInd1 = (int *) malloc(ndims * sizeof(int));
  endInd0 = (int *) malloc(ndims * sizeof(int));
  endInd1 = (int *) malloc(ndims * sizeof(int));

  /* Coordinate values at the start/end points of a boundary */
  begPos0 = (double *) malloc(ndims * sizeof(double));
  begPos1 = (double *) malloc(ndims * sizeof(double));
  endPos0 = (double *) malloc(ndims * sizeof(double));
  endPos1 = (double *) malloc(ndims * sizeof(double));

  for( i = 0; i<ndims; i++ ){
    begInd0[i] = 0;
    begInd1[i] = 0;
    endInd0[i] = 0;
    endInd1[i] = 0;
    begPos0[i] = 0;
    begPos1[i] = 0;
    endPos0[i] = 0;
    endPos1[i] = 0;
  }

  /* Heavy lifting */
  /* Loop over grids (0) */
  for( iGrid0 = 0; iGrid0 < self->ngrids; ++iGrid0 ){
    status = nccf_inq_grid_coordids( self->gridids[iGrid0], coordIds0 );

    /* Track the filenames of the grids - if blank ignore */
    file0 = ( char* )calloc( STRING_SIZE, sizeof( char ));
    status = nccf_inq_grid_name( self->gridids[iGrid0], file0 );
    nccf_li_add( &self->gridnameslist, file0 );

    /* Loop over grids (1) starting with self and don't look back. Avoids reverse
     * duplication */
    for( iGrid1 = iGrid0; iGrid1 < self->ngrids; ++iGrid1 ){

      /* Skip if same grid and no periodicity */
      if ( self->gridids[iGrid0] == self->gridids[iGrid1] && sumPeriods == 0.0 ) {
          continue;
      }
      status = nccf_inq_grid_name( self->gridids[iGrid1], file1 );
      status = nccf_inq_grid_coordids( self->gridids[iGrid1],
                  coordIds1 );

      /* Loop over boundaries (1) */
      for (iedge0 = 0; iedge0 < 2 * ndims; ++iedge0 ){
        /* fill in normVec */
        status = nccf_index2vector( iedge0, ndims, normVec0 );
        /* compute begIndex and endIndex */
        status = nccf_inq_coord_bound( coordIds0[0], normVec0,
                          begInd0, endInd0 );
          status = nccf_inq_coord_dims( coordIds0[0], dims );
          begIndex0 = nccf_get_flat_index( ndims, dims, begInd0 );
          endIndex0 = nccf_get_flat_index( ndims, dims, endInd0 );

        /* fill in start and end coordinates (1) */
        for ( i = 0; i < ndims; ++i ) {

          /* get pointer to the data */
          status = nccf_get_coord_data_pointer( coordIds0[i], &dataPtr );
          begPos0[i] = dataPtr[begIndex0];
          endPos0[i] = dataPtr[endIndex0];
        }

        /* Loop over boundaries (2) */
        for ( iedge1 = 0; iedge1 < 2 * ndims; ++iedge1 ){
          /* by default no contact */
          isContact = 0;
          /* fill in normVec */
          status = nccf_index2vector( iedge1, ndims, normVec1 );
          /* compute begIndex and endIndex */
          status = nccf_inq_coord_bound( coordIds1[0], normVec1,
                                        begInd1, endInd1 );
          status = nccf_inq_coord_dims( coordIds1[0], dims );
          begIndex1 = nccf_get_flat_index( ndims, dims, begInd1 );
          endIndex1 = nccf_get_flat_index( ndims, dims, endInd1 );
          /* fill in start and end coordinates (2) */
          for ( i = 0; i < ndims; ++i ) {
            /* get pointer to the data */
            status = nccf_get_coord_data_pointer( coordIds1[i], &dataPtr );
            begPos1[i] = dataPtr[begIndex1];
            endPos1[i] = dataPtr[endIndex1];
          }

          /* test contact
           * Don't test if the grid is the same and the edge is the same */
          if(!(( iGrid0 == iGrid1 ) && ( iedge0 == iedge1 )))
            isContact = nccf_local_check_contact( ndims, EPSLN, period,
                 begPos0, endPos0, begPos1, endPos1 );
          /* If contact fails swap begPos1 with endPos1 and retest contact */
          if( !isContact ){
            status = nccf_local_do_flipped( ndims, begPos1, endPos1 );
            if(!(( iGrid0 == iGrid1 ) && ( iedge0 == iedge1 )))
              isContact = nccf_local_check_contact( ndims, EPSLN, period,
                   begPos0, endPos0, begPos1, endPos1 );
            if( isContact ) is1Flipped = 1;
          }
          if ( isContact ) {
          /*
           * Flip only the second grid, the first is assumed to be
           * j up and i right oriented. */
            status = nccf_inq_coord_bound_slice( coordIds0[0],
                    normVec0, 0,
                    self->gs_slice_format, slice0 );
            status = nccf_inq_coord_bound_slice( coordIds1[0],
                    normVec1, is1Flipped,
                    self->gs_slice_format, slice1 );

            /* each entry must be freshly allocated,
               the desctructor will clean things up */
            contactStr = (char *)calloc(STRING_SIZE, sizeof(char));
            gridStr    = (char *)calloc(STRING_SIZE, sizeof(char));

            sprintf( contactStr, "%s%s%s", slice0,
            CF_TILE_SEPARATOR, slice1 );
            sprintf( gridStr, "%s%s%s", file0,
            CF_TILE_SEPARATOR, file1 );

            /* add contact to list */
            nccf_li_add( &self->contactindexlist, contactStr );
            nccf_li_add( &self->gridtogridlist, gridStr );

            self->ncontacts += 1;
          }
          is1Flipped = 0;
        }
      }
    }   // Grid1
  }     // Grid0

  //for (i = 0; i < ndims; ++i) {
  //  free(coordnamesbuffer[i]);
  //}
  //free(coordnamesbuffer);

  free(dims);
  free(begPos0);
  free(begPos1);
  free(endPos0);
  free(endPos1);
  free(begInd0);
  free(begInd1);
  free(endInd0);
  free(endInd1);
  free(normVec0);
  free(normVec1);
  free(file1); // Don't free file0. It is in the gridnameslist.

  return NC_NOERR;
}

