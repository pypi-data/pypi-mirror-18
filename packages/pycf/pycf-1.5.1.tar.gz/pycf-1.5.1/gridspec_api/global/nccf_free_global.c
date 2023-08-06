/*
 * API to free a global attribute object for the gridspec convention to libcf.
 *
 * $Id: nccf_free_global.c 918 2012-02-07 22:10:36Z pletzer $
 * */

#include "nccf_global.h"
#include <stdio.h>
#include <stdlib.h>

#include <nccf_varObj.h>

/**
 * \ingroup gs_global_grp
 * Free a global attribute object.
 *
 * \param globalId global ID
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_free_global(int globalId) {

    struct nccf_global_type *self;
    self = nccf_li_remove(&CFLIST_GLOBAL, globalId);
    if( nccf_li_get_nelem( &CFLIST_GLOBAL ) == 0 )
        nccf_li_del( &CFLIST_GLOBAL );
    /* Destroy the variables */
    nccf_varDestroy( &self->global );
    free(self);
    self = NULL;

    return NC_NOERR;
}

