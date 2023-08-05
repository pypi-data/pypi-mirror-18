/**
 * $Id: nccf_get_bipolar_cap.c 373 2011-01-14 19:53:49Z pletzer $
 */

#include <math.h>
#include <netcdf.h>

int nccf_get_bipolar_cap(const int dims[], 
			 double latPerim, double lonSing,
			 double lon[], double lat[]) {
  int i,j;
  latPerim = 90. - latPerim;
  double Lc, Pc;
  double L0 = 0.0; // lonSing * M_PI / 180.0;
  double di = M_PI / (dims[0]-1);
  double dj = M_PI / (dims[1]-1);
  double Pc0 = -(M_PI/2.);
  double Lc0 = -(M_PI/2.);
  double lo, la;
  for (j=0; j<dims[1]; ++j) {
    for (i=0; i<dims[0]; ++i) {
      Pc = Pc0 + j*dj;
      Lc = Lc0 + i*di;
      lo = -L0 + atan2(sin(Lc), tan(Pc));
      la = 0.5*M_PI  - 2*atan(tan(M_PI*latPerim/360.)*
			      tan(0.5*acos((cos(Lc)*cos(Pc)))));
      lon[i+j*dims[0]] = lo * 180./M_PI;
      lat[i+j*dims[0]] = la * 180./M_PI;
    }
  }
  return NC_NOERR;
}

int nccf_get_bipolar_cap2(const int dims[], 
			 double latPerim, double lonSing,
			 double lon[], double lat[]) {
  int i,j;
  latPerim = 90. - latPerim;
  double Lc, Pc;
  double L0 = 0.0; // lonSing * M_PI / 180.0;
  double di = M_PI / (dims[0]-1);
  double dj = M_PI / (dims[1]-1);
  double Pc0 = -(M_PI/2.);
  double Lc0 = -(M_PI/2.);
  double lo, la;
  for (j=0; j<dims[1]; ++j) {
    for (i=0; i<dims[0]; ++i) {
      Pc = Pc0 + j*dj;
      Lc = Lc0 + i*di;
      lo = -L0 + atan2(sin(Lc), tan(Pc));
      la = 0.5*M_PI  - 2*atan(tan(M_PI*latPerim/360.)*
			      tan(0.5*acos((cos(Lc)*cos(Pc)))));
      lon[i+j*dims[0]] = lo * 180./M_PI;
      lat[i+j*dims[0]] = la * 180./M_PI;
    }
  }
  return NC_NOERR;
}


