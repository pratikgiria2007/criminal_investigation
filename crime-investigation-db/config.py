import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-me'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'pratik'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'pratik'
    DB_NAME = os.environ.get('DB_NAME') or 'crime_db'
