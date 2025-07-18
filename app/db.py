import os

import dotenv
from pymongo import MongoClient
from pymongo.database import Database


dotenv.load_dotenv()

# MONGO_CONFIG = {
#     "host": "localhost",
#     "port": 27017,
#     "username": "root",
#     "password": "root",
# }
# client = MongoClient(**MONGO_CONFIG)


MONGODB_SRV = os.environ.get("MONGO_CONNECTION_STRING")
DB_NAME = "components"

client = MongoClient(MONGODB_SRV)
db: Database = client[DB_NAME]
