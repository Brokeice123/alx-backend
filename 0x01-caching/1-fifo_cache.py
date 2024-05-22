#!/usr/bin/env python3
"""
Fifo cache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class
    """

    def __init__(self):
        """
        Initiliaze
        """
        super().__init__()

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key)
