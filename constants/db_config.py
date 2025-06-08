import os
from dotenv import load_dotenv

load_dotenv(".env")

class DbConfig:
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")