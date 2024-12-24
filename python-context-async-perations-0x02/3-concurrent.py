import sqlite3
import asyncio
import aiosqlite

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish the database connection and create a cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def execute(self):
        # Execute the query with the provided parameters
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes (if any) and close the connection
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()

# Asynchronous functions to fetch data
async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    db_name = "alx.db"
    results = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )
    print("All users:")
    for row in results[0]:
        print(row)

    print("\nUsers older than 40:")
    for row in results[1]:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

