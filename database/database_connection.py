import psycopg2
import os
import logging
import sys
import os
import ast
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database_operations.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
# Function to establish connection to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        logging.info("Database connection established successfully.")
        return conn
    except Exception as e:
        logging.error("Error connecting to the database: %s", e)
        raise
def create_tables():
    try:
        # Establish the connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # SQL query to create telegram_data table
        create_telegram_table = """
        CREATE TABLE IF NOT EXISTS telegram_data (
            message_id TEXT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            sender TEXT NOT NULL,
            channel TEXT NOT NULL,
            text TEXT
        );
        """
        
        # SQL query to create detection_results table
        create_detection_table = """
        CREATE TABLE IF NOT EXISTS detection_results (
            id TEXT PRIMARY KEY,
            image_name TEXT NOT NULL,
            confidence_score FLOAT NOT NULL,
            class_name TEXT NOT NULL,
            bbox_coordinates TEXT NOT NULL,
            result_image_path TEXT NOT NULL
        );
        """
        
        # Execute queries
        cur.execute(create_telegram_table)
        cur.execute(create_detection_table)
        
        # Commit the changes
        conn.commit()
        logging.info("Tables successfully created.")
    except Exception as e:
        logging.error("Error creating tables: %s", e)
    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed.")

# Function to insert DataFrame into PostgreSQL
def insert_dataframe_to_db(df, table_name='telegram_data'):
    try:
        # Get a connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Define SQL query to insert data
        insert_query = f"""
            INSERT INTO {table_name} (message_id, date, sender, channel,  text)
            VALUES (%s, %s, %s, %s, %s)
        """

        # Loop through DataFrame and insert each row
        for _, row in df.iterrows():
            cur.execute(insert_query, (
                row['message_id'],
                row['date'],
                row['sender'],
                row['channel'],
                row['text']
            ))

        # Commit the transaction and close the connection
        conn.commit()
        logging.info("Data successfully inserted into the PostgreSQL database.")
    except Exception as e:
        logging.error("Error inserting data into the database: %s", e)
    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed.")

# Function to insert detection result data into PostgreSQL
def insert_detection_data(df):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO detection_results (image_name, confidence_score, class_name, bbox_coordinates, result_image_path)
            VALUES (%s, %s, %s, %s, %s)
            """
            # Iterate through the DataFrame rows and insert data into PostgreSQL
            for index, row in df.iterrows():
                # Convert bbox_coordinates to a list if it's a string representation
                if isinstance(row['bbox_coordinates'], str):
                    row['bbox_coordinates'] = ast.literal_eval(row['bbox_coordinates'])

                # Ensure bbox_coordinates is a list and convert to string with braces
                if isinstance(row['bbox_coordinates'], list):
                    bbox_coords = '{' + ','.join(map(str, row['bbox_coordinates'])) + '}'
                else:
                    raise ValueError("bbox_coordinates must be a list.")

                cursor.execute(insert_query, (
                    row['image_name'], 
                    row['confidence_score'], 
                    row['class_name'], 
                    bbox_coords,
                    row['result_image_path']
                ))

            # Commit the transaction
            conn.commit()
            cursor.close()
            print("Data successfully inserted into PostgreSQL.")
        except Exception as e:
            print(f"Error inserting data into PostgreSQL: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")