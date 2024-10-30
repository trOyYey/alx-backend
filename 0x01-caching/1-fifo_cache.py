#!/usr/bin/python3
""" FIFO module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache inheretes from BaseCaching
    """
    def __init__(self):
        """ Initiliazation
        """
        super().__init__()
        self.__queue = []

    def put(self, key, item):
        """ implementing First in
        first out caching policy
        """
        if not key or not item:
            return
        if key not in self.__queue:
            self.__queue.append(key)
        if len(self.__queue) > self.MAX_ITEMS:
            self.cache_data.pop(self.__queue[0])
            print('DISCARD: {}'.format(self.__queue.pop(0)))
        self.cache_data.update({key: item})

    def get(self, key):
        """ Get an element by it's key
        """
        return self.cache_data.get(key)
