import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Boyfaded7552",
        database="ALX_prodev"
    )
    return mydb

def stream_users():
    """Stream users from the user_data table."""
    # Connect to the database
    connection = connect_to_prodev()
    cursor = connection.cursor()

    # Execute query to fetch all rows from user_data
    cursor.execute("SELECT * FROM user_data")
    
    # Fetch and yield rows one by one
    for row in cursor:
        yield row

    # Close the cursor and connection after the loop finishes
    cursor.close()
    connection.close()
