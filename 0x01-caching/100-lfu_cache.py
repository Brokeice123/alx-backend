#!/usr/bin/env python3
"""
Module that orchestrates LFU caching strategy
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    Caching system that inherits from BaseCaching
    It applies the Least Frequently Used (LFU) algorithm
    """

    def __init__(self):
        """Initialize the LFUCache instance."""
        super().__init__()
        self.frequency = {}
        self.min_frequency = 0
        self.used_order = []

    def put(self, key, item):
        """
        Method adding an item to cache dictionary using LFU replacement
        """

        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # LFU eviction: Remove the least frequency used item
                k_v = self.frequency.items()
                min_freq_keys = \
                    [key for key, freq in k_v  if freq == self.min_frequency]
                lru_key = \
                    min(min_freq_keys, key=lambda k: self.used_order.index(k))
                del self.cache_data[lru_key]
                del self.frequency[lru_key]
                print("DISCARD:", lru_key)

            self.cache_data[key] = item
            self.frequency[key] = self.frequency.get(key, 0) + 1
            self.min_frequency = min(self.frequency.values())
            self.used_order.append(key)

    def get(self, key):
        """
        Method retrieving an item from cache dictionary
        """
        if key in self.cache_data:
            self.frequency[key] += 1
            self.min_frequency = min(self.frequency.values())
            self.used_order.remove(key)
            self.used_order.append(key)
            return self.cache_data[key]
        return None
