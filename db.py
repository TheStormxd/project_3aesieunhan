import mysql.connector
import warnings
warnings.filterwarnings('ignore')

mysql_host = "localhost"
mysql_user = "kienle"
mysql_password = "kienle201"
mysql_database = "tutor_chatbot"

try:
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        port=3306
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the query
    query = 'SELECT * FROM users'
    cursor.execute(query)

    # Fetch all rows
    result = cursor.fetchall()
    for row in result:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if cursor:  # Check if cursor is defined before closing
        cursor.close()
    if connection:  # Check if connection is defined before closing
        connection.close()
