import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')

conn = psycopg2.connect(
    host=PGHOST,
    port=PGPORT,
    database=PGDATABASE,
    user=PGUSER,
    password=PGPASSWORD
)

cursor = conn.cursor()
