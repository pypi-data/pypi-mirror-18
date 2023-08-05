/**
 * API free the host from a memory.
 *
 * "$Id: nccf_free_host.c 918 2012-02-07 22:10:36Z pletzer $"
 */

#include <nccf_host.h>
#include <netcdf.h>

/**
 * \ingroup gs_host_grp
 * Free all memory associated with a host (acts as a destructor).
 *
 * \param hostid The ID for the host object
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_free_host( int hostid ){

  struct nccf_host_type *self;

  /* Remove from list */
  self = nccf_li_remove(&CFLIST_HOST, hostid);
  if( nccf_li_get_nelem( &CFLIST_HOST ) == 0 )
        nccf_li_del( &CFLIST_HOST );

  if (self->mosaicFileBuffer) {
    free(self->mosaicFileBuffer);
    self->mosaicFileBuffer = NULL;
  }
  if (self->coordinates_id) {
    free(self->coordinates_id);
    self->coordinates_id = NULL;
  }
  if (self->data_id) {
    free(self->data_id);
    self->data_id = NULL;
  }

  /* Walk through the linked lists, remove each element and delete it */
  int index, index2;
  nccf_li_begin(&self->gridFiles);
  while (nccf_li_next(&self->gridFiles)) {
    index = nccf_li_get_id(&self->gridFiles);
    char *val = (char *) nccf_li_remove(&self->gridFiles, index);
    if (val) {
      free(val);
      val = NULL;
    }
  }
  nccf_li_begin(&self->gridNames);
  while (nccf_li_next(&self->gridNames)) {
    index = nccf_li_get_id(&self->gridNames);
    char *val = (char *) nccf_li_remove(&self->gridNames, index);
    if (val) {
      free(val);
      val = NULL;
    }
  }
  nccf_li_begin(&self->timeDataFiles);
  while (nccf_li_next(&self->timeDataFiles)) {
    index = nccf_li_get_id(&self->timeDataFiles);
    char *val = (char *) nccf_li_remove(&self->timeDataFiles, index);
    if (val) {
      free(val);
      val = NULL;
    }
  }
  nccf_li_begin(&self->statDataFiles);
  while (nccf_li_next(&self->statDataFiles)) {
    index = nccf_li_get_id(&self->statDataFiles);
    char *val = (char *) nccf_li_remove(&self->statDataFiles, index);
    if (val) {
      free(val);
      val = NULL;
    }
  }

  nccf_li_begin( &self->variables );
  while(nccf_li_next( &self->variables )){
    index = nccf_li_get_id( &self->variables );
    struct var_information *v = 
        (struct var_information *) nccf_li_remove(&self->variables, index);
    if(v){
      free(v->varname);
      v->varname = NULL;
      free(v->grid_stat_time_cat);
      v->grid_stat_time_cat = NULL;
      nccf_li_begin(&v->file_var_obj);
      while( nccf_li_next( &v->file_var_obj )){
        index2 = nccf_li_get_id( &v->file_var_obj );
        struct nccf_var_obj *f = (struct nccf_var_obj *)
                                  nccf_li_remove( &v->file_var_obj, index2 );
        if( f ) nccf_varDestroy( &f );
      }
      free(v);
      v = NULL;
    }
  }

  /* Delete the lists */
  nccf_li_del(&self->gridFiles);
  nccf_li_del(&self->gridNames);
  nccf_li_del(&self->timeDataFiles);
  nccf_li_del(&self->statDataFiles);
  nccf_li_del(&self->variables);

  free(self);
  self = NULL;

  return NC_NOERR;

}
