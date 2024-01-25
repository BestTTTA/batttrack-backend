from pymongo import MongoClient
import os

from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.environ.get('MONGO_URL', None)

client =  MongoClient(MONGO_URL)

db = client['batttrack']
users_collection = db["product_id"]