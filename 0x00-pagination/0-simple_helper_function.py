#!/usr/bin/env python3
"""
Python script that contains the simple pagination function
"""

from typing import Tuple


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
