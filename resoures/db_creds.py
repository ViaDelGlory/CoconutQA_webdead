import os
from dotenv import load_dotenv

load_dotenv()

class DataBaseCreds:
    DBNAME = os.getenv('DB_NAME')
    PORT = os.getenv('DB_PORT')
    HOST = os.getenv('DB_HOST')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')

class MoviesDbCreds:
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DATABASE_NAME = os.getenv('DB_NAME')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
