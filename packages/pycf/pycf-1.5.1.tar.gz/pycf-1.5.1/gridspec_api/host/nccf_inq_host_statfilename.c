/*
 *
 * $Id: nccf_inq_host_statfilename.c 823 2011-09-13 18:13:08Z dkindig $ 
 * */

#include <nccf_host.h>
#include <string.h>
#include <nccf_errors.h>
#include <nccf_utility_functions.h>

 /** 
  * \ingroup gs_host_grp
  * Get the file name of a static data file 
  *
  * \param hostid the ID for the host object
  * \param vfindx variable file index, ranges from 0...nstatdatafiles-1
  * \param gfindx grid file index, ranges from 0...ngrids
  * \param fname file name (output)
  * \return NC_NOERR on success
  */
int nccf_inq_host_statfilename(int hostid, int vfindx, int gfindx, 
			       char *fname) {
  int index;
  int dims[2];
  const int inx[] = {vfindx, gfindx};
  char *fn;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);
  dims[0] = self->nStatDataFiles;
  dims[1] = self->nGrids;

  // flatten the indices
  index = nccf_get_flat_index(2, dims, inx);
  fn = nccf_li_find(&self->statDataFiles, index);
  if (fn) {
    strcpy(fname, fn);
    return NC_NOERR;
  } 
  else {
    return NCCF_EINDEXOUTOFRANGE;
  }
}
