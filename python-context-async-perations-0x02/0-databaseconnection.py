import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    db_name = "alx.db"

    
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row)
