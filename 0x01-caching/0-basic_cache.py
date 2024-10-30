#!/usr/bin/python3
""" Basicach module
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache inheretes from BaseCaching
    """
    def __init__(self):
        """ Initiliazation
        """
        super().__init__()

    def put(self, key, item):
        """ Add element in the cache
        """
        if not key or not item:
            return
        self.cache_data.update({key: item})

    def get(self, key):
        """ Get an element by it's key
        """
        return self.cache_data.get(key)
