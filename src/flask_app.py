from flask import Flask, request, jsonify
import asyncio
import psycopg2
import os
from dotenv import load_dotenv

from functions import yb_like_screenshot

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

def get_db_connection():
    try:
        connection = psycopg2.connect(
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME
        )
        return connection
    except Exception as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the cjaffiliate.youtube webserver!"})

@app.route('/like-and-screenshot', methods=['GET'])
def youtube_like_and_screenshot():
    email = request.args.get('email')
    password = request.args.get('password')
    link = request.args.get('link')
    id_profile = request.args.get('id_profile')
    id_job = request.args.get('id_job')
    
    if not all([email, password, link, id_profile, id_job]):
        return jsonify({"message": "error occured cjaffiliate youtube: Missing one or more required query parameters"}), 400
    path_screenshot = asyncio.run(yb_like_screenshot(email, password, link, id_profile, id_job))
    if path_screenshot is None:
        return jsonify({"message": "error occured cjaffiliate youtube: Failed to process your request"}), 500
    return jsonify({"message": f"{path_screenshot}"})

@app.route('/trigger-function', methods=['GET'])
def trigger_function():
    # Connect to the PostgreSQL database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = connection.cursor()
    
    try:
        # Define the query to retrieve data based on fkProfiles
        fk_profiles_value = 1  # Replace with the actual fkProfiles value you want to filter by
        query = '''
        SELECT id, message, screenshot_folder, flow_process, "createdAt", "updatedAt", errors, "fkProfiles", "channel_idMessage", channel_message, "channel_peerId", "channel_editDate"
        FROM public."Job"
        WHERE "fkProfiles" = %s
        '''
        
        cursor.execute(query, (fk_profiles_value,))
        
        # Fetch all rows that match the query
        rows = cursor.fetchall()
        
        # Process the data (this is where your function logic goes)
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "message": row[1],
                "screenshot_folder": row[2],
                "flow_process": row[3],
                "createdAt": row[4],
                "updatedAt": row[5],
                "errors": row[6],
                "fkProfiles": row[7],
                "channel_idMessage": row[8],
                "channel_message": row[9],
                "channel_peerId": row[10],
                "channel_editDate": row[11]
            })
        
        return jsonify(result)
    
    except Exception as error:
        print(f"Error while executing query: {error}")
        return jsonify({"error": "Failed to execute query"}), 500
    
    finally:
        # Close the database connection
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

if __name__ == '__main__':
    app.run(debug=True)
