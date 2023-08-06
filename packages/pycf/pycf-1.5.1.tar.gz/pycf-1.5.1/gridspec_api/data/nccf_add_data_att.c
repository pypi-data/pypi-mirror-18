/**
 * $Id: nccf_add_data_att.c 929 2012-06-20 20:45:40Z pletzer $
 */

#include <nccf_data.h>

/**
 * \ingroup gs_data_grp
 * Add attribute to object.
 *
 * \param dataid data ID
 * \param name attribute name
 * \param valuep attribute value
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_add_data_att(int dataid, 
		      const char *name, const void *valuep) {

  nc_type dataType;
  struct nccf_data_type *self;
  self = nccf_li_find(&CFLIST_STRUCTURED_DATA, dataid);
  
  nccf_inq_data_type( dataid, &dataType );

  if( dataType == NC_CHAR ){
    nccf_varSetAttribText(&self->dataVar, name, (char*)valuep);
  }
  else if( dataType == NC_FLOAT ){
    nccf_varSetAttribFloat(&self->dataVar, name, *(float*)valuep);
  }
  else if( dataType == NC_DOUBLE ){
    nccf_varSetAttribDouble(&self->dataVar, name, *(double*)valuep);
  }
  else if( dataType == NC_INT ){
    nccf_varSetAttribInt(&self->dataVar, name, *(int*)valuep);
  }

  return NC_NOERR;
  
}
