import psycopg2
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the database configuration from environment variables
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=PGHOST,
    port=PGPORT,
    database=PGDATABASE,
    user=PGUSER,
    password=PGPASSWORD
)

# Create a cursor to execute SQL commands
cursor = conn.cursor()
