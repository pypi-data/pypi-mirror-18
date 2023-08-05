//
//  test1.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//


#include "cache.h" 
#include "test1.h"



 void __test1_insert_element(struct_cache* test1, cache_line* cp){
    struct test1_params* test1_params = (struct test1_params*)(test1->cache_params);
    
    gpointer key;
    if (cp->type == 'l'){
        key = (gpointer)g_new(guint64, 1);
        *(guint64*)key = *(guint64*)(cp->item_p);
    }
    else{
        key = (gpointer)g_strdup((gchar*)(cp->item_p));
    }
    
    GList* node = g_list_alloc();
    node->data = key;
    
    
    g_queue_push_tail_link(test1_params->list, node);
    g_hash_table_insert(test1_params->hashtable, (gpointer)key, (gpointer)node);
    
}

gboolean test1_check_element(struct_cache* cache, cache_line* cp){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    
    if (g_hash_table_contains(test1_params->prefetched_hashtable, cp->item_p)){
        test1_params->hit_on_prefetch += 1;
        g_hash_table_remove(test1_params->prefetched_hashtable, cp->item_p); 
    }
    
    return g_hash_table_contains( test1_params->hashtable, cp->item_p );
}


void test1_add_to_prefetch_table(struct_cache* cache, gpointer gp1, gpointer gp2){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    
    GPtrArray* pArray = g_hash_table_lookup(test1_params->next_hash,
                                            gp1
                                            );
    
    /** if we want to save space here, we can reuse the pointer from hashtable
     *  This can cut the memory usage to 1/3, but involves a hashtable look up
     *  and complicated memory free problem *******************************
     **/
    
    gpointer key2;
    if (cache->core->data_type == 'l'){
        key2 = (gpointer)g_new(guint64, 1);
        *(guint64*)key2 = *(guint64*)(gp2);
    }
    else{
        key2 = (gpointer)g_strdup((gchar*)gp2);
    }
    
    
    // insert into prefetch hashtable
    int i;
    if (pArray){
        gboolean insert = TRUE;
        if (cache->core->data_type == 'l'){
            for (i=0; i<pArray->len; i++)
                // if this element is already in the array, then don't need prefetch again
                if (*(guint64*)(g_ptr_array_index(pArray, i)) == *(guint64*)(gp2)){
                    /* update score here, not implemented yet */
                    insert = FALSE;
                    g_free(key2);
                    
                    // new 0918 change2
                    if (i==1){
                        g_ptr_array_remove_index_fast(pArray, 0);
                    }
                }
        }
        else{
            for (i=0; i<pArray->len; i++)
                // if this element is already in the cache, then don't need prefetch again
                if ( strcmp((gchar*)(g_ptr_array_index(pArray, i)), (gchar*)gp2) == 0 ){
                    /* update score here, not implemented yet */
                    insert = FALSE;
                    g_free(key2);
                    
                    // new 0918 change2
                    if (i==1){
                        g_ptr_array_remove_index_fast(pArray, 0);
                    }
                }
        }
        
        if (insert){
            if (pArray->len >= 2){
                int p = rand()%2;
                // free the content ??????????????
                //                g_free(g_ptr_array_index(pArray, p));
                g_ptr_array_remove_index_fast(pArray, p);
                
            }
            g_ptr_array_add(pArray, key2);
        }
    }
    else{
        pArray = g_ptr_array_new();                 // !!!!!!!!! not freeing memory
        g_ptr_array_add(pArray, key2);
        gpointer gp1_dup;
        if (cache->core->data_type == 'l'){
            gp1_dup = (gpointer)g_new(guint64, 1);
            *(guint64*)gp1_dup = *(guint64*)(gp1);
        }
        else{
            gp1_dup = (gpointer)g_strdup((gchar*)(gp1));
        }
        
        g_hash_table_insert(test1_params->next_hash, gp1_dup, pArray);
    }
}



void test1_prefetch(struct_cache* cache, cache_line* cp){
    /** does not support c datatype **/
    
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    
    
    
        gpointer last, current;
        if (cp->type == 'l'){
            current = (gpointer)g_new(guint64, 1);
            *(guint64*)current = *(guint64*)(cp->item_p);
            
        }
        else{
            current = (gpointer)g_strdup((gchar*)(cp->item_p));
        }
    
    
    if (test1_params->last_element){
        if (cp->type == 'l'){
            last = (gpointer)g_new(guint64, 1);
            *(guint64*)last = *(guint64*)(test1_params->last_element);
            
        }
        else{
            last = (gpointer)g_strdup((gchar*)(test1_params->last_element));
        }
        g_hash_table_insert(test1_params->next_hash, last, current);
        
        test1_add_to_prefetch_table(cache, test1_params->last_element, current);

    }

    test1_params->last_element = current;
    
    
    gpointer gp = g_hash_table_lookup(test1_params->next_hash, current);
    if (gp){
        gpointer old_key = cp->item_p;
        cp->item_p = gp;
        test1_params->num_of_check += 1;
        if (! test1_check_element(cache, cp)){
            test1_params->num_of_prefetch += 1;
            __test1_insert_element(cache, cp);            
            
            gpointer item_p;
            if (cp->type == 'l'){
                item_p = (gpointer)g_new(guint64, 1);
                *(guint64*)item_p = *(guint64*)(cp->item_p);
            }
            else
                item_p = (gpointer)g_strdup((gchar*)(cp->item_p));
            
            g_hash_table_add(test1_params->prefetched_hashtable, item_p);
            
            
        }
    cp->item_p = old_key;
      }

    
    
    
//    GPtrArray *pArray = (GPtrArray *) g_hash_table_lookup(test1_params->next_hash, current);
//    if (pArray){
//        gpointer old_key = cp->item_p;
//        int i;
//        for (i=0; i<pArray->len; i++){
//            cp->item_p = g_ptr_array_index(pArray, i);
//            test1_params->num_of_check += 1;
//            if (! test1_check_element(cache, cp)){
//                test1_params->num_of_prefetch += 1;
//                __test1_insert_element(cache, cp);
//                
//                gpointer item_p;
//                if (cp->type == 'l'){
//                    item_p = (gpointer)g_new(guint64, 1);
//                    *(guint64*)item_p = *(guint64*)(g_ptr_array_index(pArray, i));
//                }
//                else
//                    item_p = (gpointer)g_strdup((gchar*)(g_ptr_array_index(pArray, i)));
//                
//                g_hash_table_add(test1_params->prefetched_hashtable, item_p);
//            }
//        }
//        test1_params->just_prefetched = pArray;     // 0918 change2
//        cp->item_p = old_key;
//    }
//    else{
//        test1_params->just_prefetched = NULL;       // 0918 change2
//    }
}



 void __test1_update_element(struct_cache* cache, cache_line* cp){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    GList* node = (GList* ) g_hash_table_lookup(test1_params->hashtable, cp->item_p);
    g_queue_unlink(test1_params->list, node);
    g_queue_push_tail_link(test1_params->list, node);
}


 void __test1_evict_element(struct_cache* test1, cache_line* cp){
    struct test1_params* test1_params = (struct test1_params*)(test1->cache_params);
        gpointer data = g_queue_pop_head(test1_params->list);
     g_hash_table_remove(test1_params->prefetched_hashtable, data);
     g_hash_table_remove(test1_params->prefetched_hashtable, data);
        g_hash_table_remove(test1_params->hashtable, (gconstpointer)data);

}


gpointer __test1_evict_element_with_return(struct_cache* test1, cache_line* cp){
    /** evict one element and return the evicted element, needs to free the memory of returned data **/
    
    struct test1_params* test1_params = (struct test1_params*)(test1->cache_params);
    
    gpointer data = g_queue_pop_head(test1_params->list);
    
    gpointer evicted_key;
    if (cp->type == 'l'){
        evicted_key = (gpointer)g_new(guint64, 1);
        *(guint64*)evicted_key = *(guint64*)(data);
    }
    else{
        evicted_key = (gpointer)g_strdup((gchar*)data);
    }

    g_hash_table_remove(test1_params->hashtable, (gconstpointer)data);
    return evicted_key;
}




gboolean test1_add_element(struct_cache* cache, cache_line* cp){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    if (test1_check_element(cache, cp)){
        __test1_update_element(cache, cp);
        test1_prefetch(cache, cp);
        while ( (long)g_hash_table_size( test1_params->hashtable) > cache->core->size)
            __test1_evict_element(cache, cp);
        return TRUE;
    }
    else{
        __test1_insert_element(cache, cp);
        test1_prefetch(cache, cp);
        while ( (long)g_hash_table_size( test1_params->hashtable) > cache->core->size)
            __test1_evict_element(cache, cp);
        return FALSE;
    }
}




void test1_destroy(struct_cache* cache){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);

    g_queue_free(test1_params->list);
    g_hash_table_destroy(test1_params->hashtable);
    cache_destroy(cache);
}

void test1_destroy_unique(struct_cache* cache){
    /* the difference between destroy_unique and destroy
     is that the former one only free the resources that are
     unique to the cache, freeing these resources won't affect
     other caches copied from original cache
     in Optimal, next_access should not be freed in destroy_unique,
     because it is shared between different caches copied from the original one.
     */
    
    test1_destroy(cache);
}


struct_cache* test1_init(guint64 size, char data_type, void* params){
    struct_cache *cache = cache_init(size, data_type);
    cache->cache_params = g_new0(struct test1_params, 1);
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    
    cache->core->type = e_test1;
    cache->core->cache_init = test1_init;
    cache->core->destroy = test1_destroy;
    cache->core->destroy_unique = test1_destroy_unique;
    cache->core->add_element = test1_add_element;
    cache->core->check_element = test1_check_element;
    cache->core->__insert_element = __test1_insert_element;
    cache->core->__update_element = __test1_update_element;
    cache->core->__evict_element  = __test1_evict_element; 
    cache->core->get_size = test1_get_size;
    
    test1_params->last_element = NULL;
    test1_params->num_of_prefetch = 0;
    test1_params->hit_on_prefetch = 0;
    test1_params->num_of_check = 0;
    
    
    cache->core->cache_init_params = NULL;

    if (data_type == 'l'){
        test1_params->hashtable = g_hash_table_new_full(g_int64_hash, g_int64_equal, simple_g_key_value_destroyer, NULL);
        test1_params->next_hash = g_hash_table_new_full(g_int64_hash, g_int64_equal, simple_g_key_value_destroyer, simple_g_key_value_destroyer);
        test1_params->prefetched_hashtable = g_hash_table_new_full(g_int64_hash, g_int64_equal, simple_g_key_value_destroyer, NULL);
    }
    else if (data_type == 'c'){
        test1_params->hashtable = g_hash_table_new_full(g_str_hash, g_str_equal, simple_g_key_value_destroyer, NULL);
        test1_params->next_hash = g_hash_table_new_full(g_str_hash, g_str_equal, simple_g_key_value_destroyer, simple_g_key_value_destroyer);
        test1_params->prefetched_hashtable = g_hash_table_new_full(g_str_hash, g_str_equal, simple_g_key_value_destroyer, NULL);
    }
    else{
        g_error("does not support given data type: %c\n", data_type);
    }
    test1_params->list = g_queue_new();
    
    
    return cache;
}




 void test1_remove_element(struct_cache* cache, void* data_to_remove){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    
//    if (cp->type == 'l'){
        gpointer data = g_hash_table_lookup(test1_params->hashtable, data_to_remove);
        g_queue_delete_link(test1_params->list, (GList*) data);
        g_hash_table_remove(test1_params->hashtable, data_to_remove);
//    }
//    else{
//        if (strcmp((gchar*)data, ((gchar**)(test1->core->oracle))[cp->ts]) != 0)
//            test1->core->evict_err ++;
//        gpointer data_oracle = g_hash_table_lookup(test1_params->hashtable, (gpointer)((gchar**)test1->core->oracle)[cp->ts]);
//        g_hash_table_remove(test1_params->hashtable, (gpointer)((gchar**)test1->core->oracle)[cp->ts]);
//        g_queue_remove(test1_params->list, ((GList*) data_oracle)->data);
//    }

}

guint64 test1_get_size(struct_cache* cache){
    struct test1_params* test1_params = (struct test1_params*)(cache->cache_params);
    return (guint64) g_hash_table_size(test1_params->hashtable);
}
