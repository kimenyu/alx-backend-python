import sqlite3
import functools

query_cache = {}

# Decorator to manage database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[1]  # Assumes query is the second argument
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        print(f"Executing query and caching result: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
