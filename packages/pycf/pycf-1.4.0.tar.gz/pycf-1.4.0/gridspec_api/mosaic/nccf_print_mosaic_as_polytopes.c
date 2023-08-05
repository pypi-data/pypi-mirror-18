
#include "nccf_mosaic.h"

#include <stdio.h>
#include <stdlib.h>
#include "cflistitem.h"
#include <libcf_src.h>
#include "nccf_varObj.h"
#include "nccf_errors.h"
/**
 * $Id: nccf_print_mosaic_as_polytopes.c 1009 2016-10-10 07:36:12Z pletzer $
 */

struct polytope{
   int id;
   int n_supers;
   int supers[2];
};

inline double sq(double x){return x*x;}

#define nccf_print_mosaic_as_polytopes_debug
#ifdef nccf_print_mosaic_as_polytopes_debug
 #define TRD(x) fprintf(stderr,#x "=%le\n",x);
   #define TRI(x) fprintf(stderr,#x "=%i\n",x);
   #define TRA(x) fprintf(stderr,#x "=%03.1lf deg\n",x*180/M_PI);
#else
   #define TRD(x)
   #define TRI(x)
   #define TRA(x)
#endif

/**
 * \ingroup gs_mosaic_grp
 * Create a polytope file for plotting tile connectivity.
 *
 * \param contacts_id mosaic ID
 * \param file_name the .pt file name
 * \return NC_NOERR on success
 *
 * \author Andrey Sobol and David Kindig, Tech-X Corp.
 */
int nccf_print_mosaic_as_polytopes(int contacts_id, const char *file_name){

   /* Use C index ordering */
   double spread=0.1;
   int poly_id; // This has nothing to do with nccf.
   int root_poly_id;
   FILE *f=fopen(file_name,"w");
   int g; // grid index
   int d; // dimension index
   int rgb_list_size=6;
   double rgb_list[][3]=
     {  {1.0,0.5,0.25},
        {0.5,1.0,0.25},
        {1.0,0.25,0.5},
        {0.5,0.25,1.0},
        {0.25,1.0,0.5},
        {0.25,0.5,1.0},
     }
   ;

   int n_grids, n_dims;

   nccf_inq_mosaic_ngrids(contacts_id,&n_grids);
   int *grid=malloc(n_grids*sizeof(int));
   nccf_inq_mosaic_gridids(contacts_id,grid);

   /*  determining the number of dimensions. */
   nccf_inq_grid_ndims(grid[0],&n_dims);

   int *coord=malloc(sizeof(int)*n_dims);

   /* moments and shifts that are used to push the tiles apart */
   double *m0=malloc(n_grids*  sizeof(double));
   double *m1=malloc(n_grids*n_dims*sizeof(double));
   double m0t,m1t[n_dims];
   int dim[n_dims];
   int i;


   /* counting 0-polytopes i.e. How many vertices? */

   int n_vertices=0;
   for(g=0;g<n_grids;g++){
       nccf_inq_grid_coordids(grid[g],coord);
       nccf_inq_coord_dims(coord[0],dim);
       int nv=1;
       for(d=0;d<n_dims;d++){
         nv*=dim[d];
       }
       n_vertices+=nv;
   }

   struct polytope * poly=malloc(sizeof(struct polytope)*n_vertices);

   /* initialize the 0-polytopes */
   /* and calculating the moments: */
   m0t=0;
   for(d=0;d<n_dims;d++){
      m1t[d]=0;
   }

   poly_id=0;
   for(g=0;g<n_grids;g++){
      nccf_inq_grid_coordids(grid[g],coord);
      nccf_inq_coord_dims(coord[0],dim);
      int nv=1;
      double * data[n_dims];
      for(d=0;d<n_dims;d++){
         m1[g*n_dims+d]=0;
         nv*=dim[d];
         nccf_get_coord_data_pointer(coord[d],&data[d]);
      }
      for(i=0;i<nv;i++){
         //TRI(poly_id);
         poly[poly_id].n_supers=0;
         poly[poly_id].id=poly_id;
         poly_id++;
         for(d=0;d<n_dims;d++){
            m1[g*n_dims+d]+=data[d][i];
         }
      }
      m0[g]=nv;
      m0t+=m0[g];
      for(d=0;d<n_dims;d++){
         m1t[d]+=m1[g*n_dims+d];
         m1[g*n_dims+d]/=m0[g];
      }
   }
   for(d=0;d<n_dims;d++){
      m1t[d]/=m0t;
   }

   /*  process the contacts */
   int n_contacts,n_edges;
   nccf_inq_mosaic_ncontacts(contacts_id,&n_contacts);

   /* calculate the number of edges for each cell along the contact edge */
   /*  index ranges */
   int ij0_min[n_dims], ij0_max[n_dims], ij1_min[n_dims], ij1_max[n_dims];
   n_edges = 0;
   int cfo = 0;
   for (i = 0; i < n_contacts; i++) {
      int ne = 1;
      int tile0, tile1;

      nccf_inq_mosaic_gridranges(contacts_id, i,
                                  &tile0, &tile1,
                                  ij0_min, ij0_max, ij1_min, ij1_max);

      /* DNK removed +1 from this calc to get it to "C" order*/
      for (d = 0; d < n_dims; d++){
         ne *= (ij0_max[d]-ij0_min[d]+cfo);
      }
      n_edges += ne;
   }

   root_poly_id = n_vertices+n_edges;

   poly_id = n_vertices;
   for (i = 0; i < n_contacts; i++) {
      int tile0, tile1;

      /*  index ranges */
      int i0_inc[n_dims], i1_inc[n_dims];

      nccf_inq_mosaic_gridranges(contacts_id, i,
                                  &tile0, &tile1,
                                  ij0_min, ij0_max, ij1_min, ij1_max);

      for (d = 0; d < n_dims; d++) {
         i0_inc[d] = (ij0_min[d] <= ij0_max[d]? 1: -1);
         i1_inc[d] = (ij1_min[d] <= ij1_max[d]? 1: -1);
      }

      /*  this is vertex ID offset */
      int vio0 = 0, vio1 = 0;   
      
      /*  these are the dimensions of the grid */
      int dim0[d],dim1[d];

      int found = 0;
      for (g = 0; g < n_grids; g++) {
         nccf_inq_grid_coordids(grid[g],coord);
         nccf_inq_coord_dims(coord[0],dim);
         if (grid[g]==tile0){
            nccf_inq_coord_dims(coord[0],dim0);
            found=1;
            break;
         }
         int nv=1;
         for(d=0;d<n_dims;d++){
           nv*=dim[d];
         }
         vio0+=nv;
      }
      if (!found) {
         printf("Error: I was not able to match a tile with its id in"
                " nccf_print_mosaic_as_polytopes (tile0_id=%i)\n",tile0);
         return 1;
      }
      if (vio0 >= n_vertices) return NCCF_EVERTMISMATCH;

      found = 0;
      for(g = 0; g < n_grids; g++) {
         nccf_inq_grid_coordids(grid[g], coord);
         nccf_inq_coord_dims(coord[0], dim);
         if (grid[g] == tile1){
            nccf_inq_coord_dims(coord[0], dim1);
            found=1;
            break;
         }
         int nv = 1;
         for (d =0; d < n_dims; d++){
           nv *= dim[d];
         }
         vio1 += nv;
      }
      if (vio1 >= n_vertices) return NCCF_EVERTMISMATCH;
      if (!found) {
         printf("Error: I was not able to match a tile with its id in"
                " nccf_print_mosaic_as_polytopes (tile1_id=%i)\n",tile1);
         return NCCF_EVERTMISMATCH;
      }
      //TRI(tile0);
      //TRI(tile1);
      //TRI(vio0);
      //TRI(vio1);
      // assign the ranges here

      int i0[d],i1[d];
      for(d = 0;d < n_dims; d++){
         i0[d] = ij0_min[d];
         i1[d] = ij1_min[d];
      }
      int done = 0;
      while (!done) {
         int vid[2];
         vid[0] = vio0;
         vid[1] = vio1;
         int k0 = 1, k1 = 1;
         for (d = 0; d < n_dims; d++){       // C order
            vid[0] += k0*(i0[d]);
            vid[1] += k1*(i1[d]);
            k0 *= dim0[d];
            k1 *= dim1[d];
         }
         if (vid[0]>=n_vertices || vid[1]>=n_vertices) {
            TRI(vid[0]);
            TRI(vid[1]);
            for(d = 0; d < n_dims; d++) TRI(i0[d]);
            for(d = 0; d < n_dims; d++) TRI(i1[d]);
            TRI(tile0);
            TRI(tile1);
            TRI(n_vertices);
            for(g = 0; g < n_grids; g++) TRI(grid[g]);
            exit(1);
         }
         int k;
         for (k = 0; k < 2; k++) {
            int si = poly[vid[k]].n_supers;
            poly[vid[k]].supers[si] = poly_id;
            poly[vid[k]].n_supers++;
         }
         fprintf(f,"polytope %i\n",poly_id);
         fprintf(f,"facets %i %i\n",vid[0],vid[1]);
         poly_id++;

         // C
         for (d = 0; d < n_dims && i0[d]*i0_inc[d] >= (ij0_max[d]-1)*i0_inc[d]; d++) {
            i0[d] = ij0_min[d];
         }
         if (d < n_dims){  // C
            i0[d]+=i0_inc[d];
         } else {
            break;
         }
         // update i1:

         // C
         for(d=0;d < n_dims && i1[d]*i1_inc[d]>=(ij1_max[d]-1)*i1_inc[d];d++){
            i1[d]=ij1_min[d];
         }
         if (d < n_dims){    // C
            i1[d] += i1_inc[d];
         } else {
            break;
         }
      }
   }
   //TRI(poly_id);


   // printing out the vertices:
   poly_id = 0;
   for (g = 0; g < n_grids; g++){
       // int i,j,k,dim[2];
       int dim[2];
       double *coord_data[n_dims];
       nccf_inq_grid_coordids(grid[g], coord);
       nccf_inq_coord_dims(coord[0], dim);
       for (d = 0; d < n_dims; d++) {
         nccf_get_coord_data_pointer(coord[d], &coord_data[d]);
       }
       double dx[n_dims];
       int nv=1;
       for(d = 0; d < n_dims; d++) {
         dx[d] = (m1[n_dims*g+d]-m1t[d])*spread;
         nv *= dim[d];
       }
       int k;
       for (k = 0; k < nv; k++) {
            fprintf(f,"polytope %i\n",poly_id);
            fprintf(f,"coords");
            for (d = 0; d < n_dims; d++) fprintf(f," %le", coord_data[d][k] + dx[d]);
            for (   ;d<3     ;d++) fprintf(f," %le", 0.0);
            const double *rgb = rgb_list[g%rgb_list_size];
            fprintf(f,"\nvalues %le %le %le\n\n",rgb[0],rgb[1],rgb[2]);
            poly_id++;
       }
   }
   fprintf(f,"polytope %i\nfacets",root_poly_id);
   for(i = 0; i< n_edges; i++) {
      fprintf(f," %i",i+n_vertices);
   }
   fprintf(f, "\n");
   fclose(f);
   free(grid);
   free(coord);
   free(m0);
   free(m1);
   free(poly);
   return 0;
}

