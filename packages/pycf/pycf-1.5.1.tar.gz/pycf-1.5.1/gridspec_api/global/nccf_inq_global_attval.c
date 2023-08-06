/**
 * Get the name and value of a global attribute by index
 *
 * $Id: nccf_inq_global_attval.c 787 2011-07-28 19:04:22Z dkindig $
 */

#include "nccf_global.h"
#include <netcdf.h>
#include <string.h>

/**
 * \ingroup gs_global_grp
 * Get the name and value of a global attribute by index.
 *
 * \param globalid global object ID
 * \param attid attribute ID
 * \param attname Attribute name ( Returned )
 * \param attval Atttribute value ( Returned )
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_inq_global_attval(int globalid, int attid, char *attname, char *attval){

  int na;
  struct nccf_global_type *self;
  self = nccf_li_find(&CFLIST_GLOBAL, globalid);

  na = 0;
  nccf_kv_begin( &(self->global->attr) );
  while ( nccf_kv_next( &(self->global->attr) )  ) {
    if (na == attid) {
      int nelem;
      nc_type type;
      const char *name;
      const void *value;
      nccf_kv_get_key( &(self->global->attr), &name);
      nccf_kv_get_value( &(self->global->attr), name, &type, &nelem, 
			 &value);
      if (type == NC_CHAR) {
      	strcpy(attname, name);
      	strcpy(attval, value);
      }
      // need to be extended for other types of attributes (NC_FLOAT...)
      break;
    }
    na++;
  }

  return NC_NOERR;
}

