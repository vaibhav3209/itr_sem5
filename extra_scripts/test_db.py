import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables if using .env
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

# Optional: parse the URL manually
import dj_database_url
db_config = dj_database_url.parse(DATABASE_URL)

try:
    conn = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT'],
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
