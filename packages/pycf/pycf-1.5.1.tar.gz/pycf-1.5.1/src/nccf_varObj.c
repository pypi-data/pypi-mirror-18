/**
 * $Id: nccf_varObj.c 1012 2016-10-11 19:22:04Z pletzer $
 *
 * Methods to populate a netcdf-like variable in memory
 */

#include <netcdf.h>
#include <nccf_handle_error.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "nccf_varObj.h"
#include "cflistitem.h"
#include "nccf_constants.h"
#include "nccf_errors.h"

int nccf_varCreate(struct nccf_var_obj **v, const char* name) {
  int status = NC_NOERR;
  // more stuff here
  *v = malloc(sizeof(struct nccf_var_obj));
  nccf_kv_new(&(**v).attr);
  (**v).name = NULL;
  nccf_varSetVarName(v, name);
  (**v).ndims = 0;
  (**v).data_type = NC_NAT;
  (**v).dims = NULL;
  (**v).dimnames = NULL;
  (**v).data = NULL;
  (**v).save = 0;
  (**v).numWrittenRecords = 0;
  (**v).time_dimension = -1;
  return status;
}

int nccf_varCreateFromFile(struct nccf_var_obj **v, const char* name, 
         int ncid, int readData, int castToDouble) {

  // initial settings are for global attributes (name is "")
  int varid = NC_GLOBAL;
  nc_type dataType = NC_NAT;
  int ndims = 0;
  int natts = 0;

  int *dimids = NULL;
  int *dims = NULL;
  char **dimnames = NULL;

  size_t sz;
  int status;
  int i;
  int ntot;
  char *unlimdimname = calloc(NC_MAX_NAME+1, sizeof(char));

  int totError = NC_NOERR;
  nccf_varCreate(v, name);

  // determine the id of the unlimited dimension
  int unlimid; 
  status = nc_inq_unlimdim(ncid, &unlimid);
  totError += abs(status);
  if (unlimid >= 0) {
    // get the name of this dimension
    status = nc_inq_dimname(ncid, unlimid, unlimdimname);
    totError += abs(status);
  }

  // variable
  if (strcmp(name, "") != 0 && 
      nc_inq_varid(ncid, name, &varid) == NC_NOERR) {

    // only for non-global attributes

    status = nc_inq_vartype(ncid, varid, &dataType);
    (**v).data_type = dataType;
    totError += abs(status);
    status = nc_inq_varndims(ncid, varid, &ndims);
    totError += abs(status);

    // dimensions
    dimids = (int *) malloc(ndims * sizeof(int));
    dims = (int *) malloc(ndims * sizeof(int));
    dimnames = (char **) malloc(ndims * sizeof(char *));

    status = nc_inq_vardimid(ncid, varid, dimids);
    totError += abs(status);
    for (i = 0; i < ndims; ++i) {
      dimnames[i] = (char *) calloc(NC_MAX_NAME+1, sizeof(char));
      status = nc_inq_dimlen(ncid, dimids[i], &sz);
      totError += abs(status);
      status = nc_inq_dimname(ncid, dimids[i], dimnames[i]);
      totError += abs(status);
      if (strcmp(dimnames[i], unlimdimname) == 0) {
        (**v).time_dimension = i;
      }
      dims[i] = (int) sz;
    }
    status = nccf_varSetDims(v, ndims, dims, 
                             (const char **) dimnames);
    totError += abs(status);
    status = nccf_varGetNumValsPerTime(v, &ntot);
    totError += abs(status);    

    // read the first data record
    if (readData) {
      status = nccf_varReadData(v, ncid, 0, castToDouble);
      totError += abs(status);
    }
  }

  // attributes (applies to variables and global attributes)
  char attName[NC_MAX_NAME+1];
  size_t len;
  nc_type xtype;
  status = nc_inq_varnatts(ncid, varid, &natts);
  totError += abs(status);
  for (i = 0; i < natts; ++i) {
    // nc_inq_attname returns a pointer to the attr name
    // no need to allocate
    status = nc_inq_attname(ncid, varid, i, attName);
    totError += abs(status);
    status = nc_inq_att(ncid, varid, attName, &xtype, &len);
    totError += abs(status);
    if (xtype == NC_CHAR) {
      // len returned by nc_inq_attlen does no include termination
      // character
      char *attValue = (char *) calloc(len + 1, sizeof(char));
      status = nc_get_att_text(ncid, varid, attName, attValue);
      totError += abs(status);
      status = nccf_varSetAttribText(v, attName, attValue);
      totError += abs(status);
      free(attValue);
      attValue = NULL;
    }
    else if (xtype == NC_STRING) {
      char *attValue = NULL;
      /* unlike other nc_get_att methods, this will allocate memory */
      status = nc_get_att_string(ncid, varid, attName, &attValue);
      totError += abs(status);
      status = nccf_varSetAttribText(v, attName, attValue);
      totError += abs(status);
      /* reclaim memory */
      nc_free_string(len, &attValue);
    }
    else if (xtype == NC_DOUBLE) {
      double attValue[len]; 
      status = nc_get_att_double(ncid, varid, attName,
         attValue);
      totError += abs(status);
      nccf_varSetAttribDoubleArray(v, attName, len, attValue);
    }
    else if (xtype == NC_FLOAT) {
      float attValue[len]; 
      status = nc_get_att_float(ncid, varid, attName,
        attValue);
      totError += abs(status);
      nccf_varSetAttribFloatArray(v, attName, len, attValue);
    }
    else if (xtype == NC_INT) {
      int attValue[len]; 
      status = nc_get_att_int(ncid, varid, attName,
            attValue);
      totError += abs(status);
      nccf_varSetAttribIntArray(v, attName, len, attValue);
    }
    else if (xtype == NC_SHORT) {
      short attValue[len]; 
      status = nc_get_att_short(ncid, varid, attName,
        attValue);
      totError += abs(status);
      nccf_varSetAttribShortArray(v, attName, len, attValue);
    }
    else {
      // unsupported attribute type
      totError++;
    }
  }

  // clean up
  for (i = 0; i < ndims; ++i) {
    if (dimnames[i]) {
      free(dimnames[i]);
      dimnames[i] = NULL;
    }
  }
  if (dimnames) {
    free(dimnames);
    dimnames = NULL;
  }
  if (dims) {
    free(dims);
    dims = NULL;
  }
  if (dimids) {
    free(dimids);
    dimids = NULL;
  }
  if (unlimdimname) {
    free(unlimdimname);
    unlimdimname = NULL;
  }

  if (totError != NC_NOERR) {
    totError = NCCF_VAROBJCREATEFROMFILE;
  }
  return totError;
}

int nccf_varDestroy(struct nccf_var_obj **v) {
  int status = NC_NOERR;
  int i;
  for( i = 0; i < (**v).ndims; i++ ){
    free( (**v).dimnames[i] );
  }
  free((**v).dimnames);
  free((**v).dims);
  nccf_kv_del(&(**v).attr);
  if ( (**v).save ) {
    free( (**v).data );
    (**v).data = NULL;
  }
  free((**v).name);
  free(*v);
  *v = NULL;
  return status;
}

int nccf_varSetAttribText(struct nccf_var_obj **v, 
        const char *name, 
        const char *value) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_CHAR, 0, value);
  return status;
}

int nccf_varSetAttribDouble(struct nccf_var_obj **v, 
          const char *name, 
          double value) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_DOUBLE, 1, &value);
  return status;
}

int nccf_varSetAttribFloat(struct nccf_var_obj **v, 
         const char *name, 
         float value) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_FLOAT, 1, &value);
  return status;
}

int nccf_varSetAttribInt(struct nccf_var_obj **v, 
       const char *name, 
       int value) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_INT, 1, &value);
  return status;
}

int nccf_varSetAttribShort(struct nccf_var_obj **v, 
         const char *name, 
         short value) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_SHORT, 1, &value);
  return status;
}

int nccf_varSetAttribDoubleArray(struct nccf_var_obj **v, 
                                 const char *name, int n, 
                                 const double values[]) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_DOUBLE, n, values);
  return status;
}

int nccf_varSetAttribFloatArray(struct nccf_var_obj **v, 
                                const char *name, int n, 
                                const float values[]) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_FLOAT, n, values);
  return status;
}

int nccf_varSetAttribIntArray(struct nccf_var_obj **v, 
                              const char *name, int n, 
                              const int values[]) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_INT, n, values);
  return status;
}

int nccf_varSetAttribShortArray(struct nccf_var_obj **v, 
                                const char *name, int n, 
                                const short values[]) {
  int status = NC_NOERR;
  nccf_kv_add(&(**v).attr, name, NC_SHORT, n, values);
  return status;
}

int nccf_varInqAttrib(struct nccf_var_obj **v,
          const char *name, nc_type *xtypep, int *lenp) {
  int status = NC_NOERR;
  const void *value;
  nccf_kv_get_value(&(**v).attr, name, xtypep, lenp, &value);
  return status;
}

int nccf_varGetAttribPtr(struct nccf_var_obj **v, 
       const char *name, const void **value) {
  int status = NC_NOERR;
  int nelem;
  nc_type type;
  nccf_kv_get_value(&(**v).attr, name, &type, &nelem, value);
  return status;
}

int nccf_varSetDims(struct nccf_var_obj **v, 
        int numDims, const int dims[], 
        const char **dimnames) {
  int status = NC_NOERR;
  int i;
  if ((**v).dimnames) {
    for(i = 0; i < (**v).ndims; i++){
      free((**v).dimnames[i]); 
    }
  }
  (**v).ndims = numDims;
  (**v).dims = realloc((**v).dims, numDims*sizeof(int)); 
  (**v).dimnames = realloc((**v).dimnames, numDims*sizeof(char*)); 
  for(i = 0; i < numDims; i++){
    (**v).dims[i] = dims[i];
    (**v).dimnames[i] = strdup(dimnames[i]);
    if (dims[i] == NC_UNLIMITED) {
      (**v).time_dimension = i;
    }
  }
  return status;
}

int nccf_varGetDimNamePtr(struct nccf_var_obj **v, 
        int index, 
        const char **dimname ){
  int status = NC_NOERR;
  *dimname = (**v).dimnames[index];
  return status;
}

int nccf_varGetDimsPtr(struct nccf_var_obj **v, int **dims) {
  int status = NC_NOERR;
  *dims = (**v).dims;
  return status;
}

int nccf_varReadData(struct nccf_var_obj **v, int ncid, 
                     int time_index, int castToDouble) {
  int status = NC_NOERR;
  int totError = 0;
  int i;

  // get varid
  int varid = NC_GLOBAL;
  status = nc_inq_varid(ncid, (**v).name, &varid);

  // get data type
  nc_type dataType = NC_NAT;
  if (castToDouble) {
    // will cast into doubles
    dataType = NC_DOUBLE;
  }
  else {
    // get the data type from the file
    status = nc_inq_vartype(ncid, varid, &dataType);
    totError += abs(status);
  }

  void *data = NULL;
  int ndims;
  int *dims;
  status = nccf_varGetNumDims(v, &ndims);
  totError += abs(status);
  status = nccf_varGetDimsPtr(v, &dims);
  totError += abs(status);

  size_t start[ndims];
  size_t counts[ndims];
  for (i = 0; i < ndims; ++i) {
    start[i] = 0;
    counts[i] = dims[i];
    if (i == (**v).time_dimension) {
      start[i] = time_index;
      counts[i] = 1;
    }
  }
  
  int ntot;
  status = nccf_varGetNumValsPerTime(v, &ntot);
  totError += abs(status);

  // free any old data
  void *dataold = NULL;
  status = nccf_varGetDataPtr(v, &dataold);
  totError += abs(status);
  if (dataold) {
    free(dataold);
    dataold = NULL;
  }

  switch (dataType) {
  case NC_DOUBLE:
    data = malloc(sizeof(double) * ntot);
    status = nc_get_vara_double(ncid, varid, start, counts, data);
    nccf_varSetDataDouble(v, (const double *) data);
    free(data);
    data = NULL;
    break;
  case NC_FLOAT:
    data = malloc(sizeof(float) * ntot);
    status = nc_get_vara_float(ncid, varid, start, counts, data);    
    nccf_varSetDataFloat(v, (const float *) data);
    free(data);
    data = NULL;
    break;
  case NC_INT:
    data = malloc(sizeof(int) * ntot);
    status = nc_get_vara_int(ncid, varid, start, counts, data);    
    nccf_varSetDataInt(v, (const int *) data);
    free(data);
    data = NULL;
    break;
  case NC_SHORT:
    data = malloc(sizeof(short) * ntot);
    status = nc_get_vara_short(ncid, varid, start, counts, data);    
    nccf_varSetDataShort(v, (const short *) data);
    free(data);
    data = NULL;
    break;
  case NC_CHAR:
    data = calloc(ntot, sizeof(char));
    status = nc_get_vara_text(ncid, varid, start, counts, data);    
    nccf_varSetDataChar(v, (const char *) data);
    free(data);
    data = NULL;
    break;
  case NC_BYTE:
    // not implemented
    totError += 1;
    break;
  case NC_NAT:
    // not implemented
    totError += 1;
  }
  totError += abs(status);
  
  return totError;
}


int nccf_varSetDataPtr(struct nccf_var_obj **v, 
           nc_type data_type, 
           void *val) {
  int status = NC_NOERR;
  (**v).data_type = data_type;
  (**v).data = val;
  (**v).save = 0;
  return status;
}

#define _TYPE_ double
#define nccf_varSetData_TYPE_ nccf_varSetDataDouble
#define _NC_TYPE_  NC_DOUBLE
#include "nccf_varSetData_generic.h"
#undef _NC_TYPE_
#undef nccf_varSetData_TYPE_
#undef _TYPE_ 

#define _TYPE_ float
#define nccf_varSetData_TYPE_ nccf_varSetDataFloat
#define _NC_TYPE_  NC_FLOAT
#include "nccf_varSetData_generic.h"
#undef _NC_TYPE_
#undef nccf_varSetData_TYPE_
#undef _TYPE_ 

#define _TYPE_ int
#define nccf_varSetData_TYPE_ nccf_varSetDataInt
#define _NC_TYPE_  NC_INT
#include "nccf_varSetData_generic.h"
#undef _NC_TYPE_
#undef nccf_varSetData_TYPE_
#undef _TYPE_ 

#define _TYPE_ short
#define nccf_varSetData_TYPE_ nccf_varSetDataShort
#define _NC_TYPE_  NC_SHORT
#include "nccf_varSetData_generic.h"
#undef _NC_TYPE_
#undef nccf_varSetData_TYPE_
#undef _TYPE_ 

#define _TYPE_ char
#define nccf_varSetData_TYPE_ nccf_varSetDataChar
#define _NC_TYPE_  NC_CHAR
#include "nccf_varSetData_generic.h"
#undef _NC_TYPE_
#undef nccf_varSetData_TYPE_
#undef _TYPE_ 

int nccf_varGetVarNamePtr(struct nccf_var_obj **v, const char **varname) {
  int status = NC_NOERR;
  *varname=(**v).name;
  return status;
}

int nccf_varGetDataType(struct nccf_var_obj **v, nc_type *dataType) {
  int status = NC_NOERR;
  *dataType = (**v).data_type;
  return status;
}

int nccf_varGetDataPtr(struct nccf_var_obj **v, void **val) {
  int status = NC_NOERR;
  *val = (**v).data;
  return status;
}

int nccf_varGetNumValsPerTime(struct nccf_var_obj **v, int *ntot){
  int status = NC_NOERR;
  int i;
  *ntot = 1;
  for (i = 0; i < (**v).ndims; ++i) {
    if (i != (**v).time_dimension) {
      *ntot *= (**v).dims[i];
    }
  }
  return status;
}

int nccf_varGetNumDims(struct nccf_var_obj **v, int *numDims){
  int status = NC_NOERR;
  *numDims = (**v).ndims;
  return status;
}

int nccf_varSetVarName(struct nccf_var_obj **v, const char *varname) {
  int status = NC_NOERR;
  free((**v).name);
  (**v).name = strdup(varname);
  return status;
}

int nccf_varAttribIterBegin(struct nccf_var_obj **v) {
  int status = NC_NOERR;
  nccf_kv_begin(&(**v).attr);
  return status;
}

int nccf_varAttribIterNext(struct nccf_var_obj **v) {
  // return value is 1 = valid next, 0 = invalid 
  return nccf_kv_next(&(**v).attr);
}

int nccf_varInqAttribNamePtr(struct nccf_var_obj **v, 
           const char **name) {
  int status = NC_NOERR;
  nccf_kv_get_key(&(**v).attr, name);
  return status;
}

int nccf_writeListOfVars(int ncid, int numVars, ...) {
  va_list handles;
  va_start(handles, numVars);

  struct CFLISTITEM *dimNames;
  struct CFLISTITEM *dimIds;
  struct CFLISTITEM *varids, *vars;

  int status, idim, dimid;
  int varid = NC_GLOBAL;
  nc_type dataType = NC_NAT;
  int iHandle;
  int totErr = 0;
  int catchError = NC_NOERR;

  status = nc_redef(ncid);
  if (status != NC_NOERR && status != NC_EINDEFINE) {
    return status;
  }

  nccf_li_new(&vars);
  nccf_li_new(&varids); 
  nccf_li_new(&dimNames); 
  nccf_li_new(&dimIds); 

  for ( iHandle = 0; iHandle < numVars; ++iHandle) {
    struct nccf_var_obj *var = va_arg(handles, struct nccf_var_obj *);
    nccf_li_add(&vars, var);
  
    // get name and dimensions
    const char *name;
    nccf_varGetVarNamePtr(&var, &name);
    int *dims, ndims;
    nccf_varGetNumDims(&var, &ndims);
    nccf_varGetDimsPtr(&var, &dims);

    // build table of dimensions names and values and define the dimensions
    // in the netcdf file.
    int *ids = malloc(sizeof(int)*ndims);
    for (idim = 0; idim < ndims; ++idim) {
      const char *cdim;
      int dimVal = dims[idim];
      nccf_varGetDimNamePtr(&var,idim,&cdim);
      // If the value of the find is past the end of the list add a new 
      // element. This works even if the dimensions are not equal.

      int found = 0;
      nccf_li_begin(&dimNames);
      nccf_li_begin(&dimIds);
      while(nccf_li_next(&dimNames)){
        nccf_li_next(&dimIds);
        if (strcmp(dimNames->data,cdim) == 0){
           found = 1;
           ids[idim] = *(int *)dimIds->data;
           break;
        }
      } 
      if(( status = nc_inq_dimid( ncid, cdim, &dimid )) == 0 ){
        found = 1;
        ids[idim] = dimid;
      }

      if (!found) {
        // a new dimension using the dimname as the map key.
        nccf_li_add(&dimNames, strdup(cdim));
        int *id = malloc(sizeof(int));
        size_t len = (size_t) dimVal;
  nc_redef(ncid);
        status = nc_def_dim(ncid, cdim, len, id);
        totErr += abs(status);
        nccf_li_add(&dimIds, id);
        ids[idim] = *id;
     } 
    }

    // create variable
    if (strcmp(name, "") != 0) { 
      // empty string means a global attribute, with 
      // no attached data
      nccf_varGetDataType(&var, &dataType);
      if (dataType == NC_NAT) {
  catchError = NCCF_ENODATA;
      }
      nc_redef(ncid);
      status = nc_def_var(ncid, name, dataType, ndims, ids, &varid);
      totErr += abs(status);
    } else {
      varid = NC_GLOBAL;
    }

    int *id = malloc(sizeof(int));
    *id = varid;
    nccf_li_add(&varids, id);

    free(ids);
    ids = NULL;

    // attributes
    nccf_kv_begin(&(var->attr));
    while ( nccf_kv_next(&(var->attr)) ) {
      const char *attrName;
      int nelem;
      nc_type type;
      const void *attrVal;
      nccf_kv_get_key(&(var->attr), &attrName);
      nccf_kv_get_value(&(var->attr), attrName, &type, &nelem, 
      (const void **) &attrVal);
      size_t attrlen;
      status = nc_inq_attlen(ncid, varid, attrName, &attrlen);
      if (status == NC_NOERR && type == NC_CHAR) {
        // some other variable had the same attribute, so append...
        // note: + 1 because of the " " separator
        // note: + 1 because strlen does not count '\0'
        int len = attrlen + strlen( (char *) attrVal) + 1 + 1;
        char *attrValBig = (char *) calloc(len, sizeof(char));
        // attrlen may or may not include '\0'
        char *attrValOld = (char *) calloc(attrlen + 1, sizeof(char));
        status = nc_get_att_text(ncid, varid, attrName, attrValOld);
        totErr += abs(status);
        // only append if word is not in the attribute
        // use blank as word boundary
        char *blankAttrValOldBlank = (char *) calloc(strlen(attrValOld)+3, 
              sizeof(char));
        char *blankAttrVal = (char *) calloc(strlen( (char *) attrVal)+2, sizeof(char));
        char *attrValBlank = (char *) calloc(strlen( (char *) attrVal)+2, sizeof(char));
        sprintf(blankAttrValOldBlank, " %s ", attrValOld);
        sprintf(blankAttrVal, " %s", (char *) attrVal);
        sprintf(attrValBlank, "%s ", (char *) attrVal);
        if (!strstr(blankAttrValOldBlank, blankAttrVal) &&
            !strstr(blankAttrValOldBlank, attrValBlank)) {
          // append
          sprintf(attrValBig, "%s %s", attrValOld, (char *) attrVal);
          status = nc_put_att_text(ncid, varid, attrName, 
             strlen(attrValBig), attrValBig);
          totErr += abs(status);
        }
        free(blankAttrValOldBlank);
        free(blankAttrVal);
        free(attrValBlank);
         free(attrValOld);
        free(attrValBig);
      }
      else {
        // new attribute
        switch (type) {
        case NC_CHAR:
          status = nc_put_att_text(ncid, varid, attrName, 
            strlen( (char *) attrVal), 
            (char *) attrVal);
          totErr += abs(status);
          break;
        case NC_DOUBLE:
          status = nc_put_att_double(ncid, varid, attrName, NC_DOUBLE, 
             (size_t) nelem, (double *) attrVal);
          totErr += abs(status);
          break;
        case NC_FLOAT:
          status = nc_put_att_float(ncid, varid, attrName, NC_FLOAT,
            (size_t) nelem, (float *) attrVal);
          totErr += abs(status);
          break;
        case NC_INT:
          status = nc_put_att_int(ncid, varid, attrName, NC_INT,  
            (size_t) nelem, (int *) attrVal);
          totErr += abs(status);
          break;
        case NC_SHORT:
          status = nc_put_att_short(ncid, varid, attrName, NC_SHORT,  
            (size_t) nelem, (short *) attrVal);
          totErr += abs(status);
          break;
        default:
          /* unsupported attribute type */
          totErr++;
        }
      }
    }
  }

  // leave define mode
  status = nc_enddef(ncid);
  totErr += abs(status);

  // write data
  va_start(handles, numVars);
  for (iHandle = 0; iHandle < numVars; ++iHandle) {
    struct nccf_var_obj *var = va_arg(handles, struct nccf_var_obj *);
    const char *name;
    nccf_varGetVarNamePtr(&var, &name);
    if (strcmp(name, "") != 0) {
      /* only write if not global */
      nccf_writeListOfVarData(ncid, 1, var);
    }
  }

  /* clean up */
  int id;

  nccf_li_begin(&vars);
  while(nccf_li_next(&vars)){
    id = nccf_li_get_id(&vars);
    /* NO FREE HERE */
    nccf_li_remove(&vars, id);
  }
  nccf_li_del(&vars);

  nccf_li_begin(&varids);
  while(nccf_li_next(&varids)){
    id = nccf_li_get_id(&varids);
    free(nccf_li_remove(&varids, id));
  }
  nccf_li_del(&varids);

  nccf_li_begin(&dimNames);
  while(nccf_li_next(&dimNames)){
    id = nccf_li_get_id(&dimNames);
    free(nccf_li_remove(&dimNames, id));
  }
  nccf_li_del(&dimNames);

  nccf_li_begin(&dimIds);
  while( nccf_li_next(&dimIds)){
    id = nccf_li_get_id(&dimIds);
    free(nccf_li_remove(&dimIds, id));
  }
  nccf_li_del(&dimIds);

  va_end(handles);

  if (catchError != NC_NOERR) {
    // specific error
    return catchError;
  }
  else if (totErr != NC_NOERR) {
    // generic error
    return NCCF_VAROBJWRITELISTOFVARS;
  }
  // no error
  return NC_NOERR;
}

int nccf_writeListOfVarData(int ncid, int numVars, ...) {
  va_list handles;
  va_start(handles, numVars);

  int status;
  int varid;
  nc_type dataType;
  int iHandle;
  int totErr = 0;

  for (iHandle = 0; iHandle < numVars; ++iHandle) {
    struct nccf_var_obj *var = va_arg(handles, struct nccf_var_obj *);
  
    // get name and dimensions
    const char *name;
    nccf_varGetVarNamePtr(&var, &name);
    int *dims, ndims;
    nccf_varGetNumDims(&var, &ndims);
    nccf_varGetDimsPtr(&var, &dims);

    status = nc_inq_varid (ncid, name, &varid);
    totErr += abs(status);

    nccf_varGetDataType(&var, &dataType);
    size_t start[ndims];
    size_t counts[ndims];
    int i;
    for (i = 0; i < ndims; ++i) {
      start[i] = 0;
      counts[i] = dims[i];
      if (dims[i] == NC_UNLIMITED) {
      start[i] = var->numWrittenRecords;
      counts[i] = 1;
      }
    }

    void *data;
    nccf_varGetDataPtr(&var,&data);
    switch (dataType) {
    case NC_DOUBLE:
      status = nc_put_vara_double(ncid, varid, start, counts, 
          (const double *) data);
      break;
    case NC_FLOAT:
      status = nc_put_vara_float(ncid, varid, start, counts, 
         (const float *) data);
      break;
    case NC_INT:
      status = nc_put_vara_int(ncid, varid, start, counts, 
             (const int *) data);
      break;
    case NC_SHORT:
      status = nc_put_vara_short(ncid, varid, start, counts, 
         (const short *) data);
      break;
    case NC_CHAR:
      status = nc_put_vara_text(ncid, varid, start, counts, 
        (const char *)data);
      break;
    default:
      status = NC_FATAL;
    }
    totErr += abs(status);
    ++var->numWrittenRecords;
  }
  va_end(handles);

  return totErr;
}
