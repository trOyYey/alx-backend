#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
         return a dictionary with the specified key-value pairs.

        Parameters:
        index (int): starting index.
        page_size (int): number of elements to retrieve.

        Returns:
        Dict: A dictionary with the specified key-value pairs.
        """
        data = self.indexed_dataset()
        assert index < len(data)
        page_data = []
        data_len = len(data)
        i = index
        while len(page_data) < page_size and i < data_len:
            if data.get(i):
                page_data.append(data[i])
            i += 1
        dic: Dict = {
            'index': index,
            'next_index': index + page_size,
            'page_size': page_size,
            'data': page_data,
        }
        return dic
