/**
 * API write the host file from memory.
 *
 * "$Id: nccf_put_host.c 767 2011-06-06 23:20:19Z pletzer $"
 */

#include <nccf_host.h>
#include <string.h>
#include <nccf_errors.h>

/**
 * \ingroup gs_host_grp
 * Write the host to file.
 *
 * \param hostid the ID for the host object
 * \param ncid the ID for a created netcdf file.
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_put_host(int hostid, int ncid){

  int i;
  struct nccf_var_obj *mosaicFile;
  struct nccf_var_obj *vGridFiles;
  struct nccf_var_obj *vGridNames;
  struct nccf_var_obj *vStatDataFiles;
  struct nccf_var_obj *vTimeDataFiles;
  char *gridFilesBuff = NULL;
  char *gridNamesBuff = NULL;
  char *statDataFilesBuff = NULL;
  char *timeDataFilesBuff = NULL;
  int status;
  int totErr = NC_NOERR;

  struct nccf_host_type *self;
  self = nccf_li_find(&CFLIST_HOST, hostid);

  /* Build mosaic var */
  if( self->hasMosaic == 1 ){
    nccf_varCreate(&mosaicFile, CF_HOST_MOSAIC_FILENAME);
    nccf_varSetAttribText(&mosaicFile, CF_ATTNAME_CF_TYPE_NAME, 
			  CF_GS_HOST_MOSAIC_FILENAME);
    int cfDims[] = {STRING_SIZE};
    const char *cfDimNames[] = {"string"};
    nccf_varSetDims( &mosaicFile, 1, cfDims, cfDimNames );
    nccf_varSetDataPtr( &mosaicFile, NC_CHAR, self->mosaicFileBuffer );
  }

  /* build the grid names var */
  if( self->nGrids > 0 ){
    int gfDims[2] = {self->nGrids, STRING_SIZE};
    const char *gfDimNames[2] = {CF_DIMNAME_NGRIDS, CF_DIMNAME_STRING};
    gridNamesBuff = (char*)calloc( self->nGrids, STRING_SIZE*sizeof(char));
    nccf_li_begin(&self->gridNames);
    i = -1;
    while (nccf_li_next(&self->gridNames)) {
      i++;
      int index = nccf_li_get_id(&self->gridNames);
      char *fn = (char *) nccf_li_find(&self->gridNames, index);
      strcpy(&gridNamesBuff[i*STRING_SIZE], fn);
    }
    nccf_varCreate(&vGridNames, CF_HOST_TILE_NAMES);
    nccf_varSetAttribText(&vGridNames, CF_ATTNAME_CF_TYPE_NAME, 
			  CF_GS_MOSAIC_TILE_NAMES);
    nccf_varSetDims(&vGridNames, 2, gfDims, gfDimNames);
    nccf_varSetDataPtr(&vGridNames, NC_CHAR, gridNamesBuff);
  }

  /* build the grid files var */
  if( self->nGrids > 0 ){
    int gfDims[2] = {self->nGrids, STRING_SIZE};
    const char *gfDimNames[2] = {CF_DIMNAME_NGRIDS, CF_DIMNAME_STRING};
    gridFilesBuff = (char*)calloc( self->nGrids, STRING_SIZE*sizeof(char));
    nccf_li_begin(&self->gridFiles);
    i = -1;
    while (nccf_li_next(&self->gridFiles)) {
      i++;
      int index = nccf_li_get_id(&self->gridFiles);
      char *fn = (char *) nccf_li_find(&self->gridFiles, index);
      strcpy(&gridFilesBuff[i*STRING_SIZE], fn);
    }
    nccf_varCreate(&vGridFiles, CF_HOST_TILE_FILENAMES);
    nccf_varSetAttribText(&vGridFiles, CF_ATTNAME_CF_TYPE_NAME, 
			  CF_GS_HOST_TILE_FILENAMES);
    nccf_varSetDims(&vGridFiles, 2, gfDims, gfDimNames);
    nccf_varSetDataPtr(&vGridFiles, NC_CHAR, gridFilesBuff);
  }

  /* build static data files var */
  if( self->nStatDataFiles > 0 ){
    statDataFilesBuff = (char*)calloc( self->nStatDataFiles * self->nGrids, 
                                       STRING_SIZE*sizeof(char));
    nccf_li_begin(&self->statDataFiles);
    i = -1;
    while (nccf_li_next(&self->statDataFiles)) {
      i++;
      int index = nccf_li_get_id(&self->statDataFiles);
      char *fn = (char *) nccf_li_find(&self->statDataFiles, index);
      strcpy(&statDataFilesBuff[i*STRING_SIZE], fn);
    }
    nccf_varCreate(&vStatDataFiles, CF_HOST_STATDATA_FILENAME);
    nccf_varSetAttribText(&vStatDataFiles, CF_ATTNAME_CF_TYPE_NAME, 
			  CF_GS_HOST_STATDATA_FILENAME);
    int nsd = self->nStatDataFiles / self->nGrids;
    int sdDims[3] = {nsd, self->nGrids, STRING_SIZE};
    const char *sdDimNames[3] = {CF_DIMNAME_NSTATDATA, 
                                 CF_DIMNAME_NGRIDS, 
                                 CF_DIMNAME_STRING};
    nccf_varSetDims(&vStatDataFiles, 3, sdDims, sdDimNames);
    nccf_varSetDataPtr(&vStatDataFiles, NC_CHAR, statDataFilesBuff);
  }

  /* write time dependent data files */
  if( self->nTimeDataFiles > 0 ){
    timeDataFilesBuff = (char*)calloc(self->nTimeDataFiles * self->nTimeSlices * self->nGrids, 
                          STRING_SIZE*sizeof(char));
    nccf_li_begin(&self->timeDataFiles);
    i = -1;
    while (nccf_li_next(&self->timeDataFiles)) {
      i++;
      int index = nccf_li_get_id(&self->timeDataFiles);
      char *fn = (char *) nccf_li_find(&self->timeDataFiles, index);
      strcpy(&timeDataFilesBuff[i*STRING_SIZE], fn);
    }
    nccf_varCreate(&vTimeDataFiles, CF_HOST_TIMEDATA_FILENAME);
    nccf_varSetAttribText(&vTimeDataFiles, CF_ATTNAME_CF_TYPE_NAME, 
			  CF_GS_HOST_TIMEDATA_FILENAME);
    int ntd = self->nTimeDataFiles / ( self->nTimeSlices * self->nGrids );
    int tdDims[4] = {self->nTimeSlices, ntd, self->nGrids, STRING_SIZE};
    const char *tdDimNames[4] = {CF_DIMNAME_NTIMES, 
                                 CF_DIMNAME_NTIMEDATA, 
                                 CF_DIMNAME_NGRIDS, 
                                 CF_DIMNAME_STRING};
    nccf_varSetDims(&vTimeDataFiles, 4, tdDims, tdDimNames);
    nccf_varSetDataPtr(&vTimeDataFiles, NC_CHAR, timeDataFilesBuff);
  }

  /* write everything to disk */
  if (self->hasMosaic) {
    status = nccf_writeListOfVars(ncid, 1, mosaicFile);
    totErr += abs(status);
  }
  if (self->nGrids > 0) {
    status = nccf_writeListOfVars(ncid, 2, vGridNames, vGridFiles);
    totErr += abs(status);
  }
  if (self->nStatDataFiles > 0) {
    status = nccf_writeListOfVars(ncid, 1, vStatDataFiles);
    totErr += abs(status);
  }
  if (self->nTimeDataFiles > 0) {
    status = nccf_writeListOfVars(ncid, 1, vTimeDataFiles);
    totErr += abs(status);
  }

  /* clean up */
  if( self->hasMosaic ) nccf_varDestroy( &mosaicFile );
  if( gridFilesBuff ) free(gridFilesBuff);
  if( gridNamesBuff ) free(gridNamesBuff);
  
  if( self->nGrids > 0 ) nccf_varDestroy(&vGridFiles);
  if( self->nGrids > 0 ) nccf_varDestroy(&vGridNames);

  if( self->nStatDataFiles > 0 ){
    free(statDataFilesBuff);
    nccf_varDestroy(&vStatDataFiles);
  }

  if( self->nTimeDataFiles > 0 ){
    free(timeDataFilesBuff);
    nccf_varDestroy(&vTimeDataFiles);
  }

  if (totErr != NC_NOERR) {
    return NCCF_EPUTHOST;
  }
  else {
    return NC_NOERR;
  }
}


