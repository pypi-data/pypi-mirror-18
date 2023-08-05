/**
 * $Id: nccf_solve.c 848 2011-10-13 18:53:20Z pletzer $
 */

#ifdef HAVE_CONFIG_H
#include <cf_config.h>
#endif
#if (HAVE_LAPACK_NO_UNDERSCORE == 1) 
#define dGetrf dgetrf
#define dGetrs dgetrs
#define fGetrf sgetrf
#define fGetrs sgetrs
#endif
#if (HAVE_LAPACK_UNDERSCORE == 1)
#define dGetrf dgetrf_
#define dGetrs dgetrs_
#define fGetrf sgetrf_
#define fGetrs sgetrs_
#endif

#if (HAVE_LAPACK_NO_UNDERSCORE == 1 || HAVE_LAPACK_UNDERSCORE == 1)

// Lapack routines

// double
void dGetrf(int *, int *, double *, int *,  int *, int *); 
void dGetrs(char *, int *, int *, double *, int *,  int *, double *, int *, int *);
// float
void fGetrf(int *, int *, float *, int *,  int *, int *); 
void fGetrs(char *, int *, int *, float *, int *,  int *, float *, int *, int *);

#define _TYPE double
#define nccf_solve_TYPE nccf_solve_double
#define _GETRF dGetrf
#define  _GETRS dGetrs
#include <nccf_solve.h>
#undef _GETRS
#undef _GETRF
#undef nccf_solve_TYPE
#undef _TYPE

#define _TYPE float
#define nccf_solve_TYPE nccf_solve_float
#define _GETRF fGetrf
#define  _GETRS fGetrs
#include <nccf_solve.h>
#undef _GETRS
#undef _GETRF
#undef nccf_solve_TYPE
#undef _TYPE

#endif // (HAVE_LAPACK == 1 || HAVE_LAPACK_UNDERSCORE == 1)
