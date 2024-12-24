import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def execute(self):
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    db_name = "alx.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    
    with ExecuteQuery(db_name, query, params) as executor:
        results = executor.execute()


        for row in results:
            print(row)

