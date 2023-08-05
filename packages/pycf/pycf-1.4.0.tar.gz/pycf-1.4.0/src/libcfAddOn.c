/**
 * Following are some symbols that need to be resolved in order
 * for make check to work when configure'ing --enable-shared
 * This is a temporary solution!
 * $Id: libcfAddOn.c 30 2010-09-15 14:24:51Z edhartnett $
 */

#include <stdio.h>
#include "cdms.h"

// global symbols

int cuErrorOccurred;
int cuErrOpts;

void cdError(char *fmt, ...) {
  printf("in cdError...ERROR\n");
}
