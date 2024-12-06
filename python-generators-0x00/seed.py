import mysql.connector
import csv
import uuid

# Connect to MySQL server
def connect_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Boyfaded7552"
    )
    return mydb

# Create database ALX_prodev if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# Connect to the ALX_prodev database
def connect_to_prodev():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Boyfaded7552",
        database="ALX_prodev"
    )
    return mydb

# Create user_data table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age TINYINT NOT NULL
        )
    """)
    cursor.close()

# Generator to yield rows from CSV with generated user_id
def csv_row_generator(file_path):
    with open(file_path, mode='r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            user_id = str(uuid.uuid4())  # Generate a unique UUID for each row
            yield (user_id, row[0], row[1], int(row[2]))  # Convert age to an integer

# Insert data into user_data table using a generator
def insert_data(connection, csv_file_path):
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    
    try:
        # Use the generator to fetch rows
        data_gen = csv_row_generator(csv_file_path)
        cursor.executemany(insert_query, data_gen)
        connection.commit()
        
        print(f"{cursor.rowcount} records inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    
    finally:
        cursor.close()

# Main script
if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print(f"connection successful")

        connection = connect_to_prodev()

        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            cursor = connection.cursor()
            cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
            result = cursor.fetchone()
            if result:
                print(f"Database ALX_prodev is present ")
            cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()