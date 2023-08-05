/**
 * $Id: nccf_compute_regrid_weights.c 1014 2016-10-18 01:24:25Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 *
 */

#include "nccf_regrid.h"
#include <math.h>
#include <netcdf.h>

#include <nccf_coord.h>
#include <nccf_grid.h>
#include <nccf_utility_functions.h>

#define MULTIPLE_TRIALS 1
#define SNAKE 0
#define EXHAUSTIVE_SEARCH 0

int nccf_is_forbidden(int ndims, const double dIndices[], 
          struct CFLISTITEM *box_lohi) {
  int res = 0;
  int in_this_box;
  int i, id;
  int *lohi;
  nccf_li_begin(&box_lohi);
  while (nccf_li_next(&box_lohi)) {
    id = nccf_li_get_id(&box_lohi);
    lohi = nccf_li_find(&box_lohi, id);
    in_this_box = 1;
    for (i = 0; i < ndims; ++i) {
      in_this_box *= (dIndices[i] >= lohi[i] && dIndices[i] <= lohi[i + ndims]);
    }
    res += in_this_box;
  }
  return res;
}


/**
 * Starting from corners and sides, do a Newton search for dIndices. This routine can 
 * be used to overcome grid singularities at the poles.
 */
int nccf_find_indices_from_corners(int ndims, const int oriDims[], 
                                   const double ** coordOriData, 
                                   const double coord_periodicity[],
                                   const double xyz[], 
                                   int *nitermax, double *tolpos, 
                                   double dIndices[], int hit_bounds[]) {
  int status = 0;
  int numSides = 1;
  int j, i;
  int cornerVector[ndims];
  for (i = 0; i < ndims; ++i) {
    numSides *= 3;
  }
  for (j = 0; j < numSides; ++j) {
    nccf_index_to_corner_vector(j, ndims, cornerVector);
    for (i = 0; i < ndims; ++i) {
      dIndices[i] = 
        ((double) cornerVector[i] + 1.0)*
        ((double) oriDims[i] - 1.0)/2.0;
    }
    int niter = *nitermax;
    double tol = *tolpos;
    status = nccf_find_indices_double(ndims, oriDims,
                                      (const double **) coordOriData,
                                      coord_periodicity,
                                      xyz, &niter, &tol,
                                      NULL, dIndices, hit_bounds);
    if (!status) {
      /* success */
      break;
    }
  }
  return status;
}

/**
 * \ingroup gs_regrid_grp
 * Compute the weights of a regridding object.
 *
 * \param regrid_id regridding object id
 * \param nitermax maximum number of passes before failing to locate a position
 * \param tolpos tolerance in coordinate space
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_compute_regrid_weights(int regrid_id,
                                int nitermax, 
                                double tolpos) {

  int totErr = NC_NOERR;
  int status;
  int dims[] = {0, 0}, indom_dim[] = {0};
  const char *dim_names[] = {CF_DIMNAME_NTARGETS, CF_DIMNAME_NNODES};
  const char *indom_name[] = {CF_DIMNAME_NTARGETS};

  struct nccf_regrid_type *self;
  self = nccf_li_find(&CFLIST_REGRID, regrid_id);

  /* nothing to do if 0-dim */
  if (self->ndims <= 0) return NC_NOERR;

  int hit_bounds[self->ndims];

  /* get pointer to the original grid mask */
  int *imask;
  status = nccf_get_grid_mask_pointer(self->ori_grid_id, &imask);
  totErr += abs(status);

  /* get the periodicity lengths */
  double coord_periodicity[self->ndims];
  status = nccf_inq_grid_periodicity(self->ori_grid_id, 
                                     coord_periodicity);
  totErr += abs(status);

  /* fix the input */
  nitermax = (nitermax <= 0? 1: nitermax);
  tolpos = (tolpos < 1.e-15? 1.e-15: tolpos);
  int niter = nitermax;
  double tol = tolpos;
  
  int coordTargetIds[self->ndims];
  status = nccf_inq_grid_coordids(self->tgt_grid_id, coordTargetIds);
  totErr += abs(status);

  /* get the target grid dims */
  int targetDims[self->ndims];
  status = nccf_inq_coord_dims(coordTargetIds[0], targetDims);
  totErr += abs(status);

  /* get the original grid coordinates */
  int coordOriIds[self->ndims];
  status = nccf_inq_grid_coordids(self->ori_grid_id, coordOriIds);
  totErr += abs(status);

  /* get the original grid dimensions */
  int oriDims[self->ndims];
  status = nccf_inq_coord_dims(coordOriIds[0], oriDims);
  totErr += abs(status);  

  int i, j, k;
  int numNodes = 1;
  int ntot = 1;
  self->ntargets = 1;
  for (i = 0; i < self->ndims; ++i) {
    self->ntargets *= targetDims[i];
    numNodes *= 2;
    ntot *= oriDims[i];
  }
  self->nnodes = numNodes;

  /* get the original and target grid coordinates */
  double **coordOriData;
  double **coordTargetData;
  coordOriData = (double **) malloc(self->ndims * sizeof(double *));
  coordTargetData = (double **) malloc(self->ndims * sizeof(double *));
  for (i = 0; i < self->ndims; ++i) {
    double *dataPtr;
    status = nccf_get_coord_data_pointer(coordOriIds[i], &dataPtr);
    totErr += abs(status);
    coordOriData[i] = dataPtr;
    status = nccf_get_coord_data_pointer(coordTargetIds[i], &dataPtr);
    totErr += abs(status);
    coordTargetData[i] = dataPtr;
  }

  /* compute min/max values of coordinates */
  double coordOriMins[self->ndims];
  double coordOriMaxs[self->ndims];
  for (i = 0; i < self->ndims; ++i) {
    coordOriMins[i] = +CF_HUGE_DOUBLE;
    coordOriMaxs[i] = -CF_HUGE_DOUBLE;
    for (k = 0; k < ntot; ++k) {
      coordOriMins[i] = (coordOriData[i][k] < coordOriMins[i]? 
                         coordOriData[i][k]: coordOriMins[i]);
      coordOriMaxs[i] = (coordOriData[i][k] > coordOriMaxs[i]? 
                         coordOriData[i][k]: coordOriMaxs[i]);
    }
  }
  
  /* Locate the cells and compute the weights */
  double dIndices[self->ndims];
  for (i = 0; i < self->ndims; ++i) {
    /* initial guess, somewhere in the middle */
    dIndices[i] = oriDims[i]/2.13456; 
  }

  double *weights;
  weights = (double *) malloc(self->ntargets * self->nnodes * sizeof(double));
  int *lower_corner_indices;
  lower_corner_indices = (int *) malloc(self->ntargets * sizeof(int));
  char *inside_domain;
  inside_domain = (char *) malloc(self->ntargets * sizeof(char));

  int displ[self->ndims];
  int indx[self->ndims];

  int prodDims[self->ndims];
  prodDims[self->ndims - 1] = 1; 
  for (i = self->ndims - 2; i >= 0; --i) {
    prodDims[i] = prodDims[i + 1] * 2;
  }

  double xyz[self->ndims];
  int countFirstHit = 0;
  int countMultipleTrials = 0;
  for (k = 0; k < self->ntargets; ++k) {

    status = 0;

    /* Adjust the target position, taking into account that the dateline may
       may be different between the original and target grids when the 
       coordinate is periodic */

    int mod_count = 0;
    const int max_mod_count = 10; // max mod factor
    for (i = 0; i < self->ndims; ++i) {

      // set the target
      xyz[i] = coordTargetData[i][k];

      // consider adjusting if periodic
      if (coord_periodicity[i] < CF_HUGE_DOUBLE) {
        // periodic, angle-like coordinate, may need to adjust target position
        if (xyz[i] < coordOriMins[i] - tolpos &&
            xyz[i] + coord_periodicity[i] <= coordOriMaxs[i] + tolpos) {
          mod_count = 0;
          while (xyz[i] < coordOriMins[i] - tolpos && mod_count < max_mod_count) {
            xyz[i] += coord_periodicity[i];
            mod_count++;
          }
          if (mod_count >= max_mod_count) status = CF_HUGE_INT;
        }
        else if (xyz[i] > coordOriMaxs[i] + tolpos &&
                 xyz[i] - coord_periodicity[i] >= coordOriMins[i] - tolpos) {
          mod_count = 0;
          while (xyz[i] > coordOriMaxs[i] + tolpos && mod_count < max_mod_count) {
            xyz[i] -= coord_periodicity[i];
            mod_count++;
          }
          if (mod_count >= max_mod_count) status = CF_HUGE_INT;
        }
      }
    }

    /* Make sure the target position roughly lies in the original 
       grid domain, otherwise skip... */

    if (status == 0) {

      niter = nitermax;
      tol = tolpos;
      status = nccf_find_indices_double(self->ndims, oriDims, 
                                        (const double **) coordOriData, 
                                        coord_periodicity,
                                        xyz, &niter, &tol, 
                                        NULL, dIndices, hit_bounds);
      // detect if boundaries were hit, if so adjust xyz for those
      // axes that are periodic and try again
      if (status) {
        int xyzAdjusted = 0;
        for (i = 0; i < self->ndims; ++i) {
          if (hit_bounds[i] > 0 &&
              coord_periodicity[i] < CF_HUGE_DOUBLE &&
              xyz[i] - coord_periodicity[i] >= coordOriMins[i] - tolpos) {
            // subtract periodicity length
            xyz[i] -= coord_periodicity[i];
            xyzAdjusted = 1;
          }
          else if (hit_bounds[i] < 0 &&
                   coord_periodicity[i] < CF_HUGE_DOUBLE &&
                   xyz[i] + coord_periodicity[i] <= coordOriMaxs[i] + tolpos) {
            // add periodicity length
            xyz[i] += coord_periodicity[i];
            xyzAdjusted = 1;
          }
        }
        if (xyzAdjusted) {
          // now try again
          niter = nitermax;
          tol = tolpos;
          status = nccf_find_indices_double(self->ndims, oriDims, 
                                            (const double **) coordOriData, 
                                            coord_periodicity,
                                            xyz, &niter, &tol, 
                                            NULL, dIndices, hit_bounds);
        }
      }

      if (!status && nccf_is_forbidden(self->ndims, dIndices, self->box_lohi)) {
        status = -1;
      }
      if (!status) {
        countFirstHit++;
      }
#if MULTIPLE_TRIALS == 1
      /*
        A non-zero value indicates failure to find the set of (float) indices.
        This may be due to the target position being outside of the domain or
        the position was found to be in the forbidden region.
      */
      if (status) {
        niter = nitermax;
        tol = tolpos;
        status = nccf_find_indices_from_corners(self->ndims, oriDims,
                                                (const double **) coordOriData,
                                                coord_periodicity,
                                                xyz, &niter, &tol,
                                                dIndices, hit_bounds);

        if (!status && nccf_is_forbidden(self->ndims, dIndices, self->box_lohi)) {
          status = -1;
        }
        if (!status) {
          /* success */
          countMultipleTrials++;
        }
      }
#endif // MULTIPLE_TRIALS

    } // target (roughly) lies in original domain 

    inside_domain[k] = 0;
    if (status == 0) {
      inside_domain[k] = 1;
      self->nvalid++;
    }

    // compute weights
    status = nccf_get_linear_weights_double(self->ndims, oriDims,
                                            dIndices, imask, 
                                            &weights[k*self->nnodes]);
    
    // status > 0 means some masked values but interpolation was 
    // successful
    // status < 0 means too many masked values or interpolation 
    // was not successful.

    // compute the index set of the node
    for (i = 0; i < self->ndims; ++i) {
      indx[i] = (int) floor(dIndices[i]);
    }
    lower_corner_indices[k] = nccf_get_flat_index(self->ndims, 
                                                  oriDims, indx);
  }

/* Populate the data structures initialized in nccf_def_regrid */
  dims[0] = self->ntargets;
  dims[1] = numNodes;
  self->nnodes =  numNodes;
  indom_dim[0] = self->ntargets;

  nccf_varSetDims( &self->weights_stt, 2, dims, dim_names );
  nccf_varSetDataDouble( &self->weights_stt, weights );

  nccf_varSetDims( &self->lower_corner_indices_stt, 1, dims, dim_names );
  int flat_index_offsets[numNodes];
  for (j = 0; j < numNodes; ++j) {
    for (i = 0; i < self->ndims; ++i) {
      displ[i] = j / prodDims[i] % 2;
    }
    flat_index_offsets[j] = nccf_get_flat_index(self->ndims, oriDims, displ);
  }
  nccf_varSetAttribIntArray(&self->lower_corner_indices_stt,
                            CF_INDEX_OFFSETS,
                            numNodes, flat_index_offsets );
  nccf_varSetAttribIntArray(&self->lower_corner_indices_stt,
                            CF_ORI_DIMS, 
                            self->ndims, oriDims );
  nccf_varSetDataInt( &self->lower_corner_indices_stt, lower_corner_indices );

  nccf_varSetDims( &self->inside_domain_stt, 1, indom_dim, indom_name );
  nccf_varSetDataChar( &self->inside_domain_stt, inside_domain );

  /* Clean up */
  free(inside_domain);
  free(lower_corner_indices);
  free(weights);
  free(coordOriData);
  free(coordTargetData);
  
  return totErr;
}
