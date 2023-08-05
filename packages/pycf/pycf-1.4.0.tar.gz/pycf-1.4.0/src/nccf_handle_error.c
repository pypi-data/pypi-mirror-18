/*
 * Global nchandle error
 *
 * "$Id: nccf_handle_error.c 606 2011-03-25 04:11:05Z pletzer $"
 * */
#include <stdio.h>
#include <assert.h>
#include <nccf_errors.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

const char *nccf_strerror(int err);

void nccf_handle_error( const char *filename, int linenumber, int status ){

  if (status) {
    printf("In %s at line: %d, ERR = %d (netcdf: %s) (libcf: %s)\n",  
	   filename, linenumber, status, 
	   nc_strerror(status), nccf_strerror(status));
    assert(0 == 1); /* crash */
  }
}

void ncgs_handle_error( const char *filename, int linenumber, int status, 
                        const char *errmsg ){

  if (status) {
    printf( "In %s at line: %d,  %s )\n", filename, 
                                          linenumber, 
                                          errmsg );
    assert(0 == 1); /* crash */
  }
}

#ifdef __cplusplus
}
#endif /* __cplusplus */


