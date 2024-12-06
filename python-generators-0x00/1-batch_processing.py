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

def stream_users_in_batches(batch_size):
    """Fetch users in batches of the given size."""
    connection = connect_to_prodev()
    cursor = connection.cursor()

    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Process each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        filtered_users = (user for user in batch if user[3] > 25)
        yield from filtered_users

