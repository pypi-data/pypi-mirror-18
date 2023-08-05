/**
 * $Id: nccf_free_data.c 918 2012-02-07 22:10:36Z pletzer $
 */

#include <nccf_data.h>

/**
 * \ingroup gs_data_grp
 * Free object (destructor).
 *
 * \param dataid ID
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_free_data(int dataid) {

    struct nccf_data_type *self;
    self = nccf_li_remove(&CFLIST_STRUCTURED_DATA, dataid);
    if( nccf_li_get_nelem( &CFLIST_STRUCTURED_DATA ) == 0 )
        nccf_li_del( &CFLIST_STRUCTURED_DATA );

    /* Clean up */
    
    if (self->name) {
      free(self->name);
      self->name = NULL;
    }

    if (self->save) {
      if (self->data) {
        /* object owns the data */
        free(self->data);
        self->data = NULL;
      }
    }

    nccf_varDestroy(&self->dataVar);

    free(self);
    self = NULL;

    return NC_NOERR;
}
