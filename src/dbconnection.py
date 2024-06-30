import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    )
    print("PostgreSQL connection is started")
    cursor = connection.cursor()

    
    fk_profiles_value = 1
    query = '''
    SELECT id, message, screenshot_folder, flow_process, "createdAt", "updatedAt", errors, "fkProfiles", "channel_idMessage", channel_message, "channel_peerId", "channel_editDate"
    FROM public."Job"
    WHERE "fkProfiles" = %s
    '''

    cursor.execute(query, (fk_profiles_value,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as error:
    print(f"Error while connecting to PostgreSQL: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
