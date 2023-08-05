/*
 * Create pseudo-random 32 digit alpha-numeric id.
 *
 * "$Id: nccf_generate_id.c 828 2011-09-14 20:05:08Z pletzer $"
 * */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <netcdf.h>
#include <cf_config.h>
#ifdef HAVE_UUID_H
#include <uuid/uuid.h>
#endif

#include <nccf_constants.h>
#include <nccf_utility_functions.h>

time_t get_string( int ulim, char *ostr, time_t beg ){

  int i, dig;
  double sec = 0;
  int casetest;

/* Loop over the number of digits in the signature */
  for( i = 0; i < ulim; i++ ){
    sec = beg + i;
    srand48( sec );
    dig = lrand48() % 36;
    casetest = (i != 0);
    switch( casetest ){
      case 0:
        if( dig <= 9 ) sprintf( ostr, "%c", dig + 48 );
        if( dig >  9 ) sprintf( ostr, "%c", dig + 87 );
        break;
      case 1:
        if( dig <= 9 ) sprintf( ostr, "%s%c", ostr, dig + 48 );
        if( dig >  9 ) sprintf( ostr, "%s%c", ostr, dig + 87 );
        break;
    }
  }

  beg = sec;

  return( sec );

}

int nccf_generate_id(int seed_adj, char *sigid){

#ifdef HAVE_UUID_H
  char s1[37]; // 36 characters + '\0'
  uuid_t sgid;
  uuid_generate( sgid );
  uuid_unparse( sgid, s1 );
  sprintf( sigid, "%s", s1 );
#else
  time_t t1;
  char *ostr;
  ostr = ( char* )calloc( STRING_SIZE, sizeof( char ));

  ( void )time( &t1 );
  t1 = t1 / ( float )seed_adj;
  t1 = get_string( 8, ostr, t1 );
  sprintf( sigid, "%s", ostr);
  t1++;
  t1 = get_string( 4, ostr, t1 );
  sprintf( sigid, "%s-%s", sigid, ostr);
  t1++;
  t1 = get_string( 4, ostr, t1 );
  sprintf( sigid, "%s-%s", sigid, ostr);
  t1++;
  t1 = get_string( 4, ostr, t1 );
  sprintf( sigid, "%s-%s", sigid, ostr);
  t1++;
  t1 = get_string( 12, ostr, t1 );
  sprintf( sigid, "%s-%s", sigid, ostr);

  free( ostr );
#endif

  return NC_NOERR;

}
