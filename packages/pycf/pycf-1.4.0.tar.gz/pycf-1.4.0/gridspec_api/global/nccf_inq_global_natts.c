/**
 * Inquire about a global attribute
 *
 * $Id: nccf_inq_global_natts.c 738 2011-05-06 22:26:09Z edhartnett $
 */

#include "nccf_global.h"
#include <string.h>

/**
 * \ingroup gs_global_grp
 * Get the number of global attributes.
 *
 * \param globalid global object ID
 * \param natts The number of globa attributes
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_global_natts(int globalid, int *natts){

  struct nccf_global_type *self;
  int na;
  self = nccf_li_find(&CFLIST_GLOBAL, globalid);

  na = 0;
  nccf_kv_begin( &(self->global->attr) );
  while ( nccf_kv_next( &(self->global->attr) ) ) {
    na++;
  }

  *natts = na;
  
  return NC_NOERR;
}
