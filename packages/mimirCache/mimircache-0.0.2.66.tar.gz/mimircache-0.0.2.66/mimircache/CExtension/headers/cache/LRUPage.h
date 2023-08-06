//
//  LRUPage.h
//  mimircache
//
//  Created by Juncheng on 11/12/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

/** 
 this module is same as LRU, but associates a page struct with each request in the cache 
 **/



#ifndef LRUPage_h
#define LRUPage_h


#include "cache.h" 




struct LRUPage_params{
    GHashTable *hashtable;
    GQueue *list;
};


typedef struct page{
    void *key;
    void *content; 
}page_t;



extern void __LRUPage_insert_element(struct_cache* LRUPage, cache_line* cp);

extern gboolean LRUPage_check_element(struct_cache* cache, cache_line* cp);

extern void __LRUPage_update_element(struct_cache* LRUPage, cache_line* cp);

extern void __LRUPage_evict_element(struct_cache* LRUPage, cache_line* cp);

extern gboolean LRUPage_add_element(struct_cache* cache, cache_line* cp);


extern void LRUPage_destroy(struct_cache* cache);
extern void LRUPage_destroy_unique(struct_cache* cache);


struct_cache* LRUPage_init(guint64 size, char data_type, void* params);


extern void LRUPage_remove_element(struct_cache* cache, void* data_to_remove);
extern gpointer __LRUPage_evict_element_with_return(struct_cache* LRUPage, cache_line* cp);
extern guint64 LRUPage_get_size(struct_cache* cache);
extern void destroy_page(page_t *page);




#endif
