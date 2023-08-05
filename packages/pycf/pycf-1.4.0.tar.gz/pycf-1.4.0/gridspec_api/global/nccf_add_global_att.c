/**
 * Set, Append, Replace global attribute within a global object.
 *
 * $Id: nccf_add_global_att.c 836 2011-09-15 20:07:02Z pletzer $
 */

#include <string.h>

#include "nccf_global.h"
#include "nccf_errors.h"

/**
 * \ingroup gs_global_grp
 * Add a global attribute
 *
 * \param globalid global object ID
 * \param attname attribute name
 * \param attvalue attribute value
 * \param actionflag if the attribute exists, then 1 will append attvalue, 
 *        2 will replace the existing attribute value. Any other value 
 *        will leave the existing value untouched. 
 * \return NC_NOERR on success
 *
 * \author David Kindig and Alexander Pletzer, Tech-X Corp.
 */
int nccf_add_global_att(int globalid, const char *attname, const char *attvalue,
                        int actionflag ){

  struct nccf_global_type *self;
  self = nccf_li_find(&CFLIST_GLOBAL, globalid);

  int status = NC_NOERR;
  char *oldval = NULL;
  char *newval = NULL;
  int len;


  /* Append attvalue to attname using space seperation */
  switch( actionflag ){

    case 1:  /* APPEND - attvalue to end of current value after delimeter */

      status = nccf_varGetAttribPtr(&self->global, attname, 
				    (const void**) &oldval);

      /* If the attribute is empty, set it. */
      if( oldval == NULL ){
        nccf_varSetAttribText(&self->global, attname, attvalue);
        break;
      }

      /* Append otherwise */
      len = strlen( oldval );
      len += strlen( attvalue );
      newval = (char*)calloc(len+2, sizeof(char));
      strcat( newval, oldval );
      strcat( newval, " " );
      strcat( newval, attvalue );
      nccf_varSetAttribText(&self->global, attname, newval);
      oldval = NULL;
      break;

    case 2: /* Replace - Overwrite */
      status = nccf_varSetAttribText(&self->global, attname, attvalue);
      break;

    default:  /* SET - No replacement */
      len = strlen( attvalue );

      status = nccf_varGetAttribPtr( &self->global, attname, 
				     (const void**)&oldval );

      if( oldval == NULL ){
        nccf_varSetAttribText( &self->global, attname, attvalue );

      } else {
        status = NCCF_EATTEXISTS;

      }

      break;

  }

  if( newval != NULL ) free( newval );
  return status;

}

