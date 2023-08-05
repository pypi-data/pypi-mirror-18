/*
 * $Id: nccf_set_data.c 822 2011-09-13 14:39:33Z pletzer $
 */

#include <nccf_data.h>
#include <nccf_grid.h>
#include <nccf_coord.h>
#include <stdlib.h>

/**
 * \ingroup gs_data_grp
 * Set the data to a double array, this will add a new record if the 
 * data are time dependent.
 *
 * \param dataid data ID
 * \param data flat data array
 * \param save != 0 in order to copy-save the data
 * \param fill_value default value for unset data (e.g. NC_FILL_DOUBLE)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_set_data_double(int dataid, const double *data, int save, double fill_value) {
#define _type_ double
#define _nc_type_ NC_DOUBLE
#define _nccf_varSetAttribTYPE_ nccf_varSetAttribDouble
#include "nccf_set_data.h"
#undef _type_ 
#undef _nc_type_ 
#undef _nccf_varSetAttribTYPE_
}

/**
 * \ingroup gs_data_grp
 * Set the data to a float array, this will add a new record if the 
 * data are time dependent.
 *
 * \param dataid data ID
 * \param data flat data array
 * \param save != 0 in order to copy-save the data
 * \param fill_value default value for unset data (e.g. NC_FILL_FLOAT)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_set_data_float(int dataid, const float *data, int save, float fill_value) {
#define _type_ float
#define _nc_type_ NC_FLOAT
#define _nccf_varSetAttribTYPE_ nccf_varSetAttribFloat
#include "nccf_set_data.h"
#undef _type_ 
#undef _nc_type_ 
#undef _nccf_varSetAttribTYPE_
}

/**
 * \ingroup gs_data_grp
 * Set the data to an int array, this will add a new record if the 
 * data are time dependent.
 *
 * \param dataid data ID
 * \param data flat data array
 * \param save != 0 in order to copy-save the data
 * \param fill_value default value for unset data (e.g. NC_FILL_INT)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_set_data_int(int dataid, const int *data, int save, int fill_value) {
#define _type_ int
#define _nc_type_ NC_INT
#define _nccf_varSetAttribTYPE_ nccf_varSetAttribInt
#include "nccf_set_data.h"
#undef _type_ 
#undef _nc_type_ 
#undef _nccf_varSetAttribTYPE_
}

/**
 * \ingroup gs_data_grp
 * Set the data to a short array, this will add a new record if the 
 * data are time dependent.
 *
 * \param dataid data ID
 * \param data flat data array
 * \param save != 0 in order to copy-save the data
 * \param fill_value default value for unset data (e.g. NC_FILL_SHORT)
 * \return NC_NOERR on success
 *
 * \author Alexander Pletzer and David Kindig, Tech-X Corp.
 */
int nccf_set_data_short(int dataid, const short *data, int save, short fill_value) {
#define _type_ short
#define _nc_type_ NC_SHORT
#define _meth_name_ nccf_set_data_short
#define _nccf_varSetAttribTYPE_ nccf_varSetAttribShort
#include "nccf_set_data.h"
#undef _type_ 
#undef _nc_type_ 
#undef _nccf_varSetAttribTYPE_
}
