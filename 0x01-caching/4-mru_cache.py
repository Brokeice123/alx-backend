#!/usr/bin/env python3
"""
Module that orchestrates MRU caching strategy
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRU caching strategy
    """

    def __init__(self):
        """Initializing the MRUCache instance"""
        super().__init__()
        self.used_order = []

    def put(self, key, item):
        """
        Method that adds an item in the cache
        """

        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # MRU eviction: Remove the Most recently used item
                most_used_key = self.used_order.pop()
                del self.cache_data[most_used_key]
                print("DISCARD: {}". format(most_used_key))
            self.cache_data[key] = item
            self.used_order.append(key)

    def get(self, key):
        """
        Method returns the value in self.cache_data linked to key
        """

        if key in self.cache_data:
            self.used_order.remove(key)
            self.used_order.append(key)
            return self.cache_data[key]
        return None
