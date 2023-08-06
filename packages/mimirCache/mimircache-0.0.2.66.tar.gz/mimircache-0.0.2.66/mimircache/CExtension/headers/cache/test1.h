//
//  test1.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#ifndef test1_h
#define test1_h


#include "cache.h" 




struct test1_params{
    GHashTable *hashtable;
    GQueue *list;
    gpointer last_element;
    GHashTable *next_hash;
    
    GHashTable *prefetched_hashtable; 
    guint64 num_of_prefetch;
    guint64 hit_on_prefetch;
    guint64 num_of_check;
    GPtrArray *just_prefetched; 
};



extern  void __test1_insert_element(struct_cache* test1, cache_line* cp);

extern  gboolean test1_check_element(struct_cache* cache, cache_line* cp);

extern  void __test1_update_element(struct_cache* test1, cache_line* cp);

extern  void __test1_evict_element(struct_cache* test1, cache_line* cp);

extern  gboolean test1_add_element(struct_cache* cache, cache_line* cp);


extern  void test1_destroy(struct_cache* cache);
extern  void test1_destroy_unique(struct_cache* cache);


struct_cache* test1_init(guint64 size, char data_type, void* params);


extern  void test1_remove_element(struct_cache* cache, void* data_to_remove);
extern gpointer __test1_evict_element_with_return(struct_cache* test1, cache_line* cp);
extern guint64 test1_get_size(struct_cache* cache);



#endif
