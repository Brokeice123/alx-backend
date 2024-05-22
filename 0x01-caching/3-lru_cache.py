#!/usr/bin/env python3
"""
LRU cache module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRU Cache class
    """
    def __init__(self):
        """
        Initiliaze
        """
        super().__init__()
        self.used_order = []

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # lru eviction: remove the first item
                first_key = self.used_order.pop(0)
                del self.cache_data[first_key]
                print("DISCARD: {}".format(first_key))
            self.cache_data[key] = item
            self.used_order.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        self.used_order.remove(key)
        self.used_order.append(key)
        return self.cache_data[key]
