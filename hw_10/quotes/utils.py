import os
from pathlib import Path
from dotenv import load_dotenv

from pymongo import MongoClient


env_path = Path(__file__).parent.parent.parent.joinpath(".env")

if env_path.is_file():
    print("Loading environment variables from:", env_path)
    load_dotenv(env_path)
else:
    print(".env file not found. Make sure it exists in the correct location.")


MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASS = os.getenv("MONGODB_PASS")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_NAME = os.getenv("MONGODB_NAME")
URI = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOST}/{MONGODB_NAME}?retryWrites=true&w=majority"
print(f"Connecting to MongoDB with URI: {URI}")


def get_mongodb():
    client = MongoClient(URI)

    db = client[MONGODB_NAME]
    return db

