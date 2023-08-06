/**
 * $Id: nccf_keyvalue.c 940 2016-09-05 02:52:39Z pletzer $
 */

#include <stdlib.h>
#include <string.h>
#include <nccf_keyvalue.h>

void nccf_kv_new(struct CFLISTITEM **lst) {
  nccf_li_new(lst);
}

void nccf_kv_del(struct CFLISTITEM **lst) {
  nccf_li_begin(lst);
  while (nccf_li_next(lst)) {
    int id = nccf_li_get_id(lst);
    struct nccf_kv *kv = nccf_li_remove(lst, id);
    free(kv->key);
    free(kv->val);
    free(kv);
  }
  nccf_li_del(lst);  
}

void nccf_kv_get_value(struct CFLISTITEM **lst, const char *key, 
		       nc_type *type, int *nelem,  const void **val) {
  nccf_li_begin(lst);
  while (nccf_li_next(lst)) {
    struct nccf_kv *kv = (*lst)->data;
    if ( strcmp(kv->key, key) == 0 ) {
      *type = kv->type;
      *nelem = kv->nelem;
      *val = kv->val;
      return;
    }
  }
  *type = NC_NAT;
  *nelem = 0;
  *val = NULL;
}

void nccf_kv_add(struct CFLISTITEM **lst, const char *key, 
		 nc_type type, int nelem, const void *val) {
  int i;
  void *values = NULL;
  // make a copy of the data
  if (type == NC_CHAR) {
    char *vc = strdup(val);
    nelem = strlen(vc) + 1; // should we add '\0' to the length?
    values = vc;
  } 
  else if (type == NC_DOUBLE) {
    double *vd = malloc(nelem * sizeof(double));
    double *v = (double *) val;
    for (i = 0; i < nelem; ++i) {
      vd[i] = v[i];
    }
    values = vd;
  }
  else if (type == NC_FLOAT) {
    float *vf = malloc(nelem * sizeof(float));
    float *v = (float *) val;
    for (i = 0; i < nelem; ++i) {
      vf[i] = v[i];
    }
    values = vf;
  }
  else if (type == NC_INT) {
    int *vi = malloc(nelem * sizeof(int));
    int *v = (int *) val;
    for (i = 0; i < nelem; ++i) {
      vi[i] = v[i];
    }
    values = vi;
  }
  else if (type == NC_SHORT) {
    short *vi = malloc(nelem * sizeof(int));
    short *v = (short *) val;
    for (i = 0; i < nelem; ++i) {
      vi[i] = v[i];
    }
    values = vi;
  }
  else {
    // should catch this error!!
  }

  // find whether there already is an entry
  struct nccf_kv *kv2 = NULL;
  int has_key = 0;
  nccf_li_begin(lst);
  while (nccf_li_next(lst)) {
    kv2 = (*lst)->data;
    if (strcmp(kv2->key, key) == 0) {
      has_key = 1;
      break;
    }
  }
  if (has_key) {
    // replace (swap pointers)
    void *val3 = kv2->val;
    kv2->val = values;
    kv2->type = type;
    kv2->nelem = nelem;
    free(val3);
  }
  else {
    // new entry
    struct nccf_kv *kv = malloc(sizeof(struct nccf_kv));
    kv->key = strdup(key);
    kv->type = type;
    kv->nelem = nelem;
    kv->val = values;
    nccf_li_add(lst, kv);    
  }
}

void nccf_kv_begin(struct  CFLISTITEM **lst) {
  nccf_li_begin(lst);
}

int nccf_kv_next(struct  CFLISTITEM **lst) {
   return nccf_li_next(lst);
}

void nccf_kv_get_key(struct  CFLISTITEM **lst, const char **key) {
  if (*lst) {
    struct nccf_kv *kv = (*lst)->data;
    *key = kv->key;
  }
}
