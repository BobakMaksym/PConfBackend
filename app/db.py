import os

import dotenv
from pymongo import MongoClient
from pymongo.database import Database


dotenv.load_dotenv()


MONGODB_SRV = os.environ.get("MONGO_CONNECTION_STRING")
DB_NAME = "components"

client = MongoClient(MONGODB_SRV, uuidRepresentation="standard")
db: Database = client[DB_NAME]
