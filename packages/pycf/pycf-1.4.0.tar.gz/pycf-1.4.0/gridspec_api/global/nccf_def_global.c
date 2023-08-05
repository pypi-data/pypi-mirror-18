/**
 * API to define a global object for the gridspec convention to libcf.
 *
 * $Id: nccf_def_global.c 738 2011-05-06 22:26:09Z edhartnett $
 */

#include "nccf_global.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <nccf_handle_error.h>
#include <nccf_varObj.h>

struct CFLISTITEM *CFLIST_GLOBAL;

/*! \defgroup gs_global_grp Global attribute object
  \ingroup gridspec_grp

An object to set, append or replace global attributes. One object can be created
per file to be written.
*/

/**
 * \ingroup gs_global_grp
 * Define a global attribute object (acts as a constructor).
 *
 * \param globalid (output) global ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_def_global( int *globalid ){
 
  /* Instantiate object */
    struct nccf_global_type *self;
    self = (struct nccf_global_type *)
             malloc(sizeof(struct nccf_global_type));

    /* Global attributes */
    nccf_varCreate(&self->global, CF_GLOBAL );

    if( CFLIST_GLOBAL == NULL ) nccf_li_new( &CFLIST_GLOBAL );

    *globalid = nccf_li_add( &CFLIST_GLOBAL, self );

    return NC_NOERR;

}
