//
//  LRUPage.h
//  mimircache
//
//  Created by Juncheng on 6/2/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//


#include "cache.h" 
#include "LRUPage.h"



void __LRUPage_insert_element(struct_cache* LRUPage, cache_line* cp){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(LRUPage->cache_params);
    
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
    
    
    g_queue_push_tail_link(LRUPage_params->list, node);
    g_hash_table_insert(LRUPage_params->hashtable, (gpointer)key, (gpointer)node);
    
}

gboolean LRUPage_check_element(struct_cache* cache, cache_line* cp){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    return g_hash_table_contains( LRUPage_params->hashtable, cp->item_p );
}


void __LRUPage_update_element(struct_cache* cache, cache_line* cp){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    GList* node = (GList* ) g_hash_table_lookup(LRUPage_params->hashtable, cp->item_p);
    g_queue_unlink(LRUPage_params->list, node);
    g_queue_push_tail_link(LRUPage_params->list, node);
}


void __LRUPage_evict_element(struct_cache* LRUPage, cache_line* cp){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(LRUPage->cache_params);

    if (LRUPage->core->cache_debug_level == 2){     // compare to Oracle
        while (cp->ts > g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos)){
            if ( g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos) -
                g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos-1) != 0 ){
                
                LRUPage->core->evict_err_array[LRUPage->core->bp_pos-1] = LRUPage->core->evict_err /
                    (g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos) -
                        g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos-1));
                LRUPage->core->evict_err = 0;
            }
            else
                LRUPage->core->evict_err_array[LRUPage->core->bp_pos-1] = 0;
            
            LRUPage->core->evict_err = 0;
            LRUPage->core->bp_pos++;
        }
        
        if (cp->ts == g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos)){
            LRUPage->core->evict_err_array[LRUPage->core->bp_pos-1] = (double)LRUPage->core->evict_err /
            (g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos) -
             g_array_index(LRUPage->core->bp->array, guint64, LRUPage->core->bp_pos-1));
            LRUPage->core->evict_err = 0;
            LRUPage->core->bp_pos ++;
        }
            
        gpointer data = g_queue_peek_head(LRUPage_params->list);
        if (cp->type == 'l'){
            if (*(guint64*)(data) != ((guint64*)LRUPage->core->oracle)[cp->ts]){
                printf("error at %lu, LRUPage: %lu, Optimal: %lu\n", cp->ts, *(guint64*)(data), ((guint64*)LRUPage->core->oracle)[cp->ts]);
                LRUPage->core->evict_err ++;
            }
            else
                printf("no error at %lu: %lu, %lu\n", cp->ts, *(guint64*)(data), *(guint64*)(g_queue_peek_tail(LRUPage_params->list)));
            gpointer data_oracle = g_hash_table_lookup(LRUPage_params->hashtable, (gpointer)&((guint64* )LRUPage->core->oracle)[cp->ts]);
            g_queue_delete_link(LRUPage_params->list, (GList*)data_oracle);
//            g_queue_remove(LRUPage_params->list, ((GList*) data_oracle)->data);
            g_hash_table_remove(LRUPage_params->hashtable, (gpointer)&((guint64*)LRUPage->core->oracle)[cp->ts]);
        }
        else{
            if (strcmp((gchar*)data, ((gchar**)(LRUPage->core->oracle))[cp->ts]) != 0)
                LRUPage->core->evict_err ++;
            gpointer data_oracle = g_hash_table_lookup(LRUPage_params->hashtable, (gpointer)((gchar**)LRUPage->core->oracle)[cp->ts]);
            g_hash_table_remove(LRUPage_params->hashtable, (gpointer)((gchar**)LRUPage->core->oracle)[cp->ts]);
            g_queue_remove(LRUPage_params->list, ((GList*) data_oracle)->data);
        }
        
    }
    
    else if (LRUPage->core->cache_debug_level == 1){
        // record eviction list
        
        gpointer data = g_queue_pop_head(LRUPage_params->list);
        if (cp->type == 'l'){
            ((guint64*)(LRUPage->core->eviction_array))[cp->ts] = *(guint64*)(data);
        }
        else{
            gchar* key = g_strdup((gchar*)(data));
            ((gchar**)(LRUPage->core->eviction_array))[cp->ts] = key;
        }

        g_hash_table_remove(LRUPage_params->hashtable, (gconstpointer)data);
    }

    
    else{
        gpointer data = g_queue_pop_head(LRUPage_params->list);
        g_hash_table_remove(LRUPage_params->hashtable, (gconstpointer)data);
    }
}


gpointer __LRUPage_evict_element_with_return(struct_cache* LRUPage, cache_line* cp){
    /** evict one element and return the evicted element, needs to free the memory of returned data **/
    
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(LRUPage->cache_params);
    
    gpointer data = g_queue_pop_head(LRUPage_params->list);
    
    gpointer evicted_key;
    if (cp->type == 'l'){
        evicted_key = (gpointer)g_new(guint64, 1);
        *(guint64*)evicted_key = *(guint64*)(data);
    }
    else{
        evicted_key = (gpointer)g_strdup((gchar*)data);
    }

    g_hash_table_remove(LRUPage_params->hashtable, (gconstpointer)data);
    return evicted_key;
}




gboolean LRUPage_add_element(struct_cache* cache, cache_line* cp){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    if (LRUPage_check_element(cache, cp)){
        __LRUPage_update_element(cache, cp);
        return TRUE;
    }
    else{
        __LRUPage_insert_element(cache, cp);
        if ( (long)g_hash_table_size( LRUPage_params->hashtable) > cache->core->size)
            __LRUPage_evict_element(cache, cp);
        return FALSE;
    }
}




void LRUPage_destroy(struct_cache* cache){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);

//    g_queue_free(LRUPage_params->list);                 // Jason: should call g_queue_free_full to free the memory of node content
    // 0921
    g_queue_free(LRUPage_params->list);
    g_hash_table_destroy(LRUPage_params->hashtable);
    cache_destroy(cache);
}

void LRUPage_destroy_unique(struct_cache* cache){
    /* the difference between destroy_unique and destroy
     is that the former one only free the resources that are
     unique to the cache, freeing these resources won't affect
     other caches copied from original cache
     in Optimal, next_access should not be freed in destroy_unique,
     because it is shared between different caches copied from the original one.
     */
    
    LRUPage_destroy(cache);
}


struct_cache* LRUPage_init(guint64 size, char data_type, void* params){
    struct_cache *cache = cache_init(size, data_type);
    cache->cache_params = g_new0(struct LRUPage_params, 1);
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    
    cache->core->type = e_LRUPage;
    cache->core->cache_init = LRUPage_init;
    cache->core->destroy = LRUPage_destroy;
    cache->core->destroy_unique = LRUPage_destroy_unique;
    cache->core->add_element = LRUPage_add_element;
    cache->core->check_element = LRUPage_check_element;
    cache->core->__insert_element = __LRUPage_insert_element;
    cache->core->__update_element = __LRUPage_update_element;
    cache->core->__evict_element  = __LRUPage_evict_element;
    cache->core->__evict_element_with_return = __LRUPage_evict_element_with_return; 
    cache->core->get_size = LRUPage_get_size; 
    cache->core->cache_init_params = NULL;

    if (data_type == 'l'){
        LRUPage_params->hashtable = g_hash_table_new_full(g_int64_hash, g_int64_equal, simple_g_key_value_destroyer, NULL);
    }
    else if (data_type == 'c'){
        LRUPage_params->hashtable = g_hash_table_new_full(g_str_hash, g_str_equal, simple_g_key_value_destroyer, NULL);
    }
    else{
        g_error("does not support given data type: %c\n", data_type);
    }
    LRUPage_params->list = g_queue_new();
    
    
    return cache;
}




 void LRUPage_remove_element(struct_cache* cache, void* data_to_remove){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    
//    if (cp->type == 'l'){
        gpointer data = g_hash_table_lookup(LRUPage_params->hashtable, data_to_remove);
        g_queue_delete_link(LRUPage_params->list, (GList*) data);
        g_hash_table_remove(LRUPage_params->hashtable, data_to_remove);
//    }
//    else{
//        if (strcmp((gchar*)data, ((gchar**)(LRUPage->core->oracle))[cp->ts]) != 0)
//            LRUPage->core->evict_err ++;
//        gpointer data_oracle = g_hash_table_lookup(LRUPage_params->hashtable, (gpointer)((gchar**)LRUPage->core->oracle)[cp->ts]);
//        g_hash_table_remove(LRUPage_params->hashtable, (gpointer)((gchar**)LRUPage->core->oracle)[cp->ts]);
//        g_queue_remove(LRUPage_params->list, ((GList*) data_oracle)->data);
//    }

}

guint64 LRUPage_get_size(struct_cache* cache){
    struct LRUPage_params* LRUPage_params = (struct LRUPage_params*)(cache->cache_params);
    return (guint64) g_hash_table_size(LRUPage_params->hashtable);
}


void destroy_page(page_t *page){
    if (page->key != NULL)
        g_free(page->key);
    if (page->content != NULL)
        g_free(page->content); 
}
