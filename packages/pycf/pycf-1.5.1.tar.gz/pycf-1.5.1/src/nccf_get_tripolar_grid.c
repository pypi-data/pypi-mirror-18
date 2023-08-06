/**
 * $Id: nccf_get_tripolar_grid.c 373 2011-01-14 19:53:49Z pletzer $
 */

#include <math.h>
#include <netcdf.h>

int nccf_get_tripolar_grid(const int dims[], int capIndx,
    double lon[], double lat[]) {
  int i,j;
  double L, P, Lc, Pc, Pc0, Lc0, latPerim;
  double L0 = 0.;
  double di = 2*M_PI / (dims[0]-1);
  double dj = M_PI / (dims[1]-1);

  Pc0 = -0.5*M_PI;
  Lc0 = -M_PI;

  for (j=0; j < capIndx; ++j) {
    for (i=0; i<dims[0]; ++i) {
      P = Pc0 + j*dj;
      L = Lc0 + i*di;
      lon[i+j*dims[0]] = L;
      lat[i+j*dims[0]] = P;

      lon[i+j*dims[0]] *= 180./M_PI;
      lat[i+j*dims[0]] *= 180./M_PI;
    }
  }

  latPerim = M_PI - capIndx*dj;
  //di = M_PI / (dims[0]-1);
  dj = (0.5*M_PI) / (dims[1]-capIndx-1);
  Pc0 = -(M_PI/2.);
  Lc0 = (M_PI/2.);
  for (j=capIndx; j<dims[1]; ++j) {
    for (i=0; i<dims[0]/2; ++i) {
      Pc = Pc0 + i*di;
      Lc = Lc0 - (j-capIndx)*dj;
      lon[i+j*dims[0]] = L0 - atan2(sin(Lc), tan(Pc));
      lat[i+j*dims[0]] = 0.5*M_PI  - 2.*atan(tan(latPerim/2.)*
          tan(0.5*acos((cos(Lc)*cos(Pc)))));

      lon[i+j*dims[0]] *= 180./M_PI;
      lat[i+j*dims[0]] *= 180./M_PI;
    }
  }

  Pc0 = -(M_PI/2.);
  Lc0 = -(M_PI/2.);
  for (j=capIndx; j<dims[1]; ++j) {
    for (i=dims[0]/2; i<dims[0]; ++i) {
      Pc = Pc0 + (dims[0]-i-1)*di;
      Lc = Lc0 + (1-1.e-10)*(j-capIndx)*dj;
      lon[i+j*dims[0]] = L0 - atan2(sin(Lc), tan(Pc));
      lat[i+j*dims[0]] = 0.5*M_PI  - 2.*atan(tan(latPerim/2.)*
          tan(0.5*acos((cos(Lc)*cos(Pc)))));

      lon[i+j*dims[0]] *= 180./M_PI;
      lat[i+j*dims[0]] *= 180./M_PI;
    }
  }
  return NC_NOERR;
}
