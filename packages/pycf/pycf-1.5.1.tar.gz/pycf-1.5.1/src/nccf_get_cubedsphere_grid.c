/**
 * $Id: nccf_get_cubedsphere_grid.c 373 2011-01-14 19:53:49Z pletzer $
 */

#include <math.h>
#include <netcdf.h>

double nccf_norm(double v[]) {
  return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

void nccf_cross_product(double v[], const double w[], double res[]) {
  res[0] = v[1]*w[2] - v[2]*w[1];
  res[1] = v[2]*w[0] - v[0]*w[2];
  res[2] = v[0]*w[1] - v[1]*w[0];
}

int nccf_get_cubedsphere_grid(const int dims[], const int faceVect[], 
			      double lon[], double lat[]) {

  int i,j,n;
	double iUnit[3];
	double jUnit[3];
	double tempVec[3];

	for (n=0; n<3; ++n)
		tempVec[n] = (double) faceVect[n];

	iUnit[0] = (double) faceVect[2];
	iUnit[1] = (double) faceVect[0];
	iUnit[2] = (double) faceVect[1];

	nccf_cross_product(tempVec, iUnit, jUnit);

	for (n=0; n<3; ++n) {
		// start position in corner
		tempVec[n] -= (iUnit[n] + jUnit[n]);
		// shrink unit vectors down to gridspacing-size
		iUnit[n] *= 2./(dims[0]-1);
		jUnit[n] *= 2./(dims[1]-1);
	}

	double x,y,z;
	for (j=0; j<dims[1]; ++j) {
		for (i=0; i<dims[0]; ++i) {
			x = tempVec[0] + i*iUnit[0] + j*jUnit[0];
			y = tempVec[1] + i*iUnit[1] + j*jUnit[1];
			z = tempVec[2] + i*iUnit[2] + j*jUnit[2];
			lon[i + j*dims[0]] = atan2(y,x) * (180./M_PI);
			lat[i + j*dims[0]] = atan2(z, sqrt(pow(x,2) + 
					pow(y,2))) * (180./M_PI);
		}
	}

  return NC_NOERR;
}
