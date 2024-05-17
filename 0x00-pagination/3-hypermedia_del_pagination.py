#!/usr/bin/env python3
"""
Python script that contains the simple pagination function
"""

import csv
import math
from typing import Dict, Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end index for a given page and page size.

      Args:
          page: The current page number (1-indexed).
          page_size: The number of items per page.

      Returns:
          A tuple containing the start (inclusive) and end (exclusive) indexes
          for the requested page.
    """
    return ((page - 1) * page_size, page * page_size)


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
        """
        get_page
        """
        
        assert(isinstance(page, int) and isinstance(page_size, int))
        assert(page > 0 and page_size > 0)
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start > len(data):
            return []
        return data[start: end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, int]:
        """Returns a dictionary containing hypermedia links for pagination.

        Args:
            page: The page number (default: 1).
            page_size: The number of items per page (default: 10).

        Returns:
            A dictionary containing the following key-value pairs:
                page_size: the length of the returned dataset page
                page: the current page number
                data: the dataset page (equivalent to the return from get_page)
                next_page: the number of the next page, None if no next page
                prev_page: the number of the previous page, None if no previous page
                total_pages: the total number of pages in the dataset as an integer
        """

        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing hypermedia links for pagination
        resilient to data deletions.

        Args:
            index: The starting index for pagination (default: None).
            page_size: The number of items per page (default: 10).

        Returns:
            A dictionary containing the following key-value pairs:
                index: The current start index of the returned page.
                next_index: The next index to query with.
                page_size: The current page size.
                data: The actual page of the dataset.
        """

        assert index is None or 0 <= index < len(self.indexed_dataset), "index out of range"

        if index is None:
            index = 0

        data = []
        current_index = index
        for _ in range(page_size):
            if current_index in self.indexed_dataset:
                data.append(self.indexed_dataset[current_index])
            current_index += 1

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": current_index
        }