/**
 * API for adding/removing and extracting elements from a linked list
 * $Id: cflistitem.c 924 2012-03-23 16:47:05Z pletzer $
 */

/* std includes */
#include <stdlib.h>

#include "cflistitem.h"
#include "nccf_errors.h"

/* Private method, only called internally to create a new item 
   in an existing list  */
void 
nccf_li_newitem(struct CFLISTITEM **lst, int id) {
  *lst = (struct CFLISTITEM *) malloc(sizeof(struct CFLISTITEM));
  (*lst)->first = *lst; // will be reset by the user
  (*lst)->next = NULL;
  (*lst)->data = NULL;
  (*lst)->id = id;
}

void 
nccf_li_new(struct CFLISTITEM **lst) {
  nccf_li_newitem(lst, CF_LIST_ITEM_HEAD_ID);
  // create head
  // data stores the number of items (in head)
  (*lst)->data = (int *) malloc( sizeof( int ) );
  int *nelemp;
  nelemp = (int *) (*lst)->data; // cast into int pointer
  *nelemp = 0;
}

void
nccf_li_del(struct CFLISTITEM **lst) {
  if (*lst) {
    free((*lst)->data);
    free(*lst);
  }
  *lst = NULL;
}

void 
nccf_li_begin(struct CFLISTITEM **lst){
  *lst = (*lst)->first;
}

int 
nccf_li_next(struct CFLISTITEM **lst) {
  if (!(*lst)) return 0;
  if ((*lst)->next) {
    *lst = (*lst)->next;
    return 1;
  }
  return 0;
}

int 
nccf_li_get_id(struct CFLISTITEM **lst) {
  return (*lst)->id;
}

int
nccf_li_add(struct CFLISTITEM **lst, const _DATATYPE *data){
  struct CFLISTITEM *newItem;
  struct CFLISTITEM *fstItem;
  int maxid;

  /* advance to the last item */
  while ((*lst)->next) {
    *lst = (*lst)->next;
  }
  maxid = nccf_li_get_nelem( lst );

  /* create new entry */
  nccf_li_newitem(&newItem, maxid);
  newItem->first = (*lst)->first;
  newItem->data = (void *) data;

  /* Update the number of elements */
  int *nelemp;
  fstItem = (*lst)->first;
  nelemp = (int*)fstItem->data;
  ( *nelemp )++;
  
  /* set item to new entry */
  (*lst)->next = newItem;
  (*lst) = newItem;
  return newItem->id;
}

int
nccf_li_get_nelem( struct CFLISTITEM **lst ){
  int *nelemp;
  struct CFLISTITEM *fstItem;

  fstItem = (*lst)->first;
  nelemp = (int*)fstItem->data;
  return *nelemp;
}

int 
nccf_li_insert_after( struct CFLISTITEM **lst, const _DATATYPE *data, 
                int id){

  /* The list to be inserted ( new )*/
  struct CFLISTITEM *insertItem;
  struct CFLISTITEM *fstItem;
  int maxId;

  /* Find the id after which the new element is to be inserted */
  maxId = nccf_li_get_nelem( lst );
  nccf_li_begin(lst);
  if( id != CF_LIST_ITEM_HEAD_ID ){
    while(nccf_li_next(lst)){
      if ((*lst)->id == id) break;
    }
  }

  nccf_li_newitem( &insertItem, maxId );

  /* Populate the inserted list item */
  insertItem->first = (*lst)->first;
  insertItem->data = (void*)data;
  insertItem->id = maxId;

  /* Switch where the next item of the current item points */
  insertItem->next = (*lst)->next;
  (*lst)->next = insertItem;

  /* Update the number of elements */
  int *nelemp;
  fstItem = (*lst)->first;
  nelemp = (int*)fstItem->data;
  ( *nelemp )++;
  
  /* Output the inserted items ID */
  return insertItem->id;
}

int 
nccf_li_insert( struct CFLISTITEM **lst, 
                const _DATATYPE *data,
                int (*comparison)(const _DATATYPE *data1, const _DATATYPE *data2), 
                int ifresult0 ){

  /* The list to be inserted ( new )*/
  _DATATYPE *curData;
  int useId = CF_LIST_ITEM_HEAD_ID;
  int curId = CF_LIST_ITEM_HEAD_ID;
  int id = NCCF_LISTITEMEXISTS, result = 0;


  /* advance to the last item */
  nccf_li_begin(lst);
  while( nccf_li_next(lst)){
    curId = nccf_li_get_id( lst );
    curData = (_DATATYPE *)nccf_li_find( lst, curId );
    result = comparison( data, curData );

    /* data < curData */
    if( result < 0 ) break;
    /* data > curData */ 
    if( result > 0) useId = curId;
    if( result == 0 && ifresult0 != 0 ) useId = curId;
  }
  if( ifresult0 || result != 0 ) id = nccf_li_insert_after( lst, data, useId );

  return id;
}

_DATATYPE *
nccf_li_remove(struct CFLISTITEM **lst, int id){
  _DATATYPE *data = NULL;
  if (id == CF_LIST_ITEM_HEAD_ID) {
    /* this call will not remove the head, use 
       nccf_li_delete to remove head */
    return NULL;
  }
  nccf_li_begin(lst);
  struct CFLISTITEM *prevItem = *lst;
  struct CFLISTITEM *firstItem;
  while (nccf_li_next(lst)) {
    if ((*lst)->id == id) {

      /* Decrement the number of elements */
      int *nelemp;
      firstItem = (*lst)->first;
      nelemp = (int *) firstItem->data; // cast into int pointer
      --(*nelemp);
      
      /* Change where next is pointing */
      prevItem->next = (*lst)->next;
      data = (*lst)->data;

      free(*lst); 
      *lst = NULL;
      break;
    }
    prevItem = *lst;
  }
  *lst = prevItem;
  return data;
}

_DATATYPE *
nccf_li_find(struct CFLISTITEM **lst, int id){

  /* may already be pointing to the searched element */
  if ((*lst)->id == id) {
    return (*lst)->data;
  }

  /* reset only if searched id is smaller than pointed id */
  if ( (*lst)->id > id ) {
    nccf_li_begin(lst);
  }

  /* locate id and return element */
  while (nccf_li_next(lst)) {
    if ((*lst)->id == id) {
      return (*lst)->data;
    }
  }

  /* no element found */
  return NULL;
}
