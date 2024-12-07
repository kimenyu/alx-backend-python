#!/usr/bin/python3
import seed

def stream_user_ages():
    """
    Generator to stream user ages from the database one by one.
    :yield: Age of the next user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate the average age using the stream_user_ages generator.
    Prints the average age of users.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
