#!/usr/bin/env python3
"""
0-simple_helper_function module
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''
    return a tuple of size two containing a start index and an end index.

    Parameters:
    page (int): page number.
    page_size (int): number of elements per page.

    Returns:
    return a tuple of size two containing a start index and an end index.
    '''
    start_index: int = (page - 1) * page_size
    return (start_index, start_index + page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''
        get_page that takes two integer arguments page AND page_size.

        Parameters:
        page (int): page number.
        page_size (int): number of elements per page.

        Returns:
        List[List]: A list of lists containing the  data for the requested
        page by the specified page size.
        '''
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        start_index, end_index = index_range(page, page_size)
        book: List[List] = self.dataset()
        if start_index >= len(book):
            return []
        return book[start_index: end_index]
