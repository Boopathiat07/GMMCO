import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None
