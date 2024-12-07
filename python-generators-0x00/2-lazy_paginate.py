#!/usr/bin/python3
import seed

def lazy_paginate(page_size):
    """
    Lazily fetch and paginate data from the user_data table.
    :param page_size: Number of rows to fetch per page.
    """
    offset = 0
    while True:
        # Fetch the next page using the paginate_users function
        page = paginate_users(page_size, offset)
        if not page:
            break  # Exit when there are no more rows to fetch
        yield page
        offset += page_size  # Increment the offset for the next page


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the user_data table.
    :param page_size: Number of rows to fetch.
    :param offset: Starting point for fetching rows.
    :return: List of rows fetched.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows
