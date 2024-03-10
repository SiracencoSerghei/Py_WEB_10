import os
import json
from pathlib import Path
from bson.objectid import ObjectId
from dotenv import load_dotenv

from  pymongo import MongoClient


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

def add_quotes_to_mongo():
    client = None
    try:
        # client = MongoClient("mongodb://localhost:54321")
        print(URI)
        client = MongoClient(URI)

        db = client[MONGODB_NAME]

        with open('data/quotes.json', 'r', encoding='utf-8') as fd:
            quotes = json.load(fd)

        for quote in quotes:
            author = db.authors.find_one({'fullname': quote['author']})
            if author:
                db.quotes.insert_one({
                    'quote': quote['quote'],
                    'tags': quote['tags'],
                    'author': ObjectId(author['_id'])
                })
        print("Data insertion successful.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    add_quotes_to_mongo()
    