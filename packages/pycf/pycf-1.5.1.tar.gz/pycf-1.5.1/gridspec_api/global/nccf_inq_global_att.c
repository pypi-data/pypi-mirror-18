/**
 * Inquire about a global attribute by name
 *
 * $Id: nccf_inq_global_att.c 787 2011-07-28 19:04:22Z dkindig $
 */

#include "nccf_global.h"
#include <string.h>

/**
 * \ingroup gs_global_grp
 * Get a global attribute value from its name
 *
 * \param globalid global object ID
 * \param name attribute name to retrieve
 * \param value attribute value, must have size NC_MAX_NAME or larger
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_global_att(int globalid, const char *name, char *value){

  struct nccf_global_type *self;
  self = nccf_li_find(&CFLIST_GLOBAL, globalid);
  const char *tmp = NULL;
  nccf_varGetAttribPtr(&self->global, name, (const void **) &tmp);
  if( tmp != NULL ) strcpy( value, tmp );
  
  return NC_NOERR;
}


